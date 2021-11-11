import csv
import contextlib
import io
import re
from unittest import mock

import flask
from keg import signals
from werkzeug.datastructures import MultiDict
import wrapt
import xlrd

from pyquery import PyQuery


def inrequest(*req_args, **req_kwargs):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        with flask.current_app.test_request_context(*req_args, **req_kwargs):
            return wrapped(*args, **kwargs)
    return wrapper


@contextlib.contextmanager
def app_config_cli(**kwargs):
    """
        Set config values on any apps instantiated while the context manager is active.
        This is intended to be used with cli tests where the `current_app` in the test will be
        different from the `current_app` when the CLI command is invoked, making it very difficult
        to dynamically set app config variables using mock.patch.dict like we normally would.
        Example::
        class TestCLI(CLIBase):
            app_cls = RaceBetter
            def test_it(self):
                with testing.app_config_cli(FOO_NAME='Bar'):
                    result = self.invoke('echo-foo-name')
                assert 'Bar' in result.output
    """

    @signals.config_complete.connect
    def set_config(app):
        app.config.update(kwargs)

    yield


@contextlib.contextmanager
def app_config(**kwargs):
    """ Just a shortcut for mock.patch.dict...
            def test_it(self):
                with testing.app_config(FOO_NAME='Bar'):
                    assert flask.current_app.config['FOO_NAME'] == 'Bar'
    """
    with mock.patch.dict(flask.current_app.config, **kwargs) as mocked_config:
        yield mocked_config


def mock_patch_obj(*args, **kwargs):
    kwargs.setdefault('autospec', True)
    kwargs.setdefault('spec_set', True)
    return mock.patch.object(*args, **kwargs)


def mock_patch(*args, **kwargs):
    kwargs.setdefault('autospec', True)
    kwargs.setdefault('spec_set', True)
    return mock.patch(*args, **kwargs)


def iter_pyq(pyq):
    """Iterates over the children of a PyQuery ojbect and converts each child to another PyQuery
    object."""
    return [pyq.eq(ix) for ix in range(len(pyq))]


def default_assert_fn(x, y):
    assert x == y


def assert_rendered_xls_matches(rendered_xls, xls_headers, xls_rows):
    """
    Verifies that `rendered_xls` has a set of headers and values that match
    the given parameters.
    NOTE: This method does not perform in-depth analysis of complex workbooks!
          Multiple worksheets or complex (multi-row) headers *are not verified!*
    NOTE: This method should be added directly to webgrid. While we wait for
          upstream changes, however, we can use this here.
    :param rendered_xls:
    :param xls_headers:
    :param xls_rows:
    :return:
    :rtype: bool
    """
    assert bool(rendered_xls) is True
    workbook = xlrd.open_workbook(file_contents=rendered_xls)

    assert workbook.nsheets >= 1
    sheet = workbook.sheet_by_index(0)

    # # verify the shape of the sheet

    # ## shape of rows (1 row for the headers, 1 for each row of data)
    nrows = len(xls_rows)
    if xls_headers:
        nrows += 1
    assert nrows == sheet.nrows

    # ## shape of columns
    ncols = max(
        len(xls_headers) if xls_headers else 0,
        max(len(values) for values in xls_rows) if xls_rows else 0
    )
    assert ncols == sheet.ncols

    if xls_headers:
        assert tuple(cell.value for cell in sheet.row(0)) == tuple(xls_headers)

    if xls_rows:
        row_iter = sheet.get_rows()

        # skip header row
        if xls_headers:
            next(row_iter)

        for row, expected_row in zip(row_iter, xls_rows):
            actual_row = tuple(
                xlrd.xldate.xldate_as_datetime(cell.value, workbook.datemode)
                if cell.ctype == xlrd.XL_CELL_DATE else cell.value
                for cell in row
            )
            assert actual_row == tuple(expected_row)


class GridAssertions(object):
    """Encapsulates common assertions on Grids."""

    def __init__(self, grid):
        """Takes a grid factory function and defers its creation until necessary."""
        self.grid = grid
        self._pyq = None

    @property
    def pyq(self):
        self._pyq = self._pyq or PyQuery(self.grid.html())
        return self._pyq

    def get_column_pyq(self, column_index):
        """Returns PyQuery objects for each row in the given column (0-based index)."""
        return iter_pyq(self.pyq('table.records tbody tr td:eq({})'.format(column_index)))

    def get_actions(self):
        """Returns a list of PyQuery objects for each action link in the action column."""
        return [iter_pyq(row('a')) for row in self.get_column_pyq(0)]

    def get_action_titles(self):
        """Returns the a list of title attributes for each link in each row of the action column."""
        return [[a.attr('title') for a in row] for row in self.get_actions()]

    def get_header_row(self):
        return self.pyq.find('table.records thead th')

    def check_headers(self, actual, expected, assert_fn=default_assert_fn):
        assert len(actual) == len(expected)

        for i, v in enumerate(expected):
            assert_fn(actual.eq(i).text(), v)

    def check_row(self, actual, expected, assert_fn=default_assert_fn, headers=None):
        len_mismatch_msg = 'Row %i has {actual} items {expected} was expected.'

        assert len(actual) == len(expected), \
            len_mismatch_msg.format(actual=len(actual), expected=len(expected))

        for i, expected_value in enumerate(expected):
            try:
                actual_value = actual.eq(i).text()
                assert_fn(actual_value, expected_value)
            except AssertionError as e:
                column_name = headers[i] if headers else 'unknown'
                message_fmt = ('Failed Grid Assertion: '
                               'Row %i column {item_num} "{column}" doesn\'t match expected. '
                               'Expecting {e_value} ({e_type}) got {a_value} ({a_type}). '
                               '\n Full message: "{msg}"')

                message = message_fmt.format(item_num=i, column=column_name, msg=str(e),
                                             e_value=expected_value, e_type=type(expected_value),
                                             a_value=actual_value, a_type=type(actual_value))
                raise AssertionError(message)

    def assert_rendered_xls_matches(self, xls_headers, xls_values):
        """
        Assert that the grid's rendered XLS matches the expected headers and values.
        :param xls_headers:
        :param xls_values:
        :return:
        """

        # render the grid to XLS
        workbook = self.grid.xlsx()
        workbook.filename.seek(0)

        # verify that the rendered XLS matches the expected values
        assert_rendered_xls_matches(workbook.filename.getvalue(), xls_headers, xls_values)

    def assert_rendered_csv_matches(self, expect):
        for idx, row in enumerate(self.csv()):
            assert row == expect[idx]

    def assert_grid_matches(self, expect, with_subtotals=False):
        def assert_matches(actual, expect):
            if isinstance(expect, re.compile('').__class__):
                assert expect.match(actual)
            else:
                assert str(expect) == actual

        rows = self.pyq.find('table.records tbody tr')
        if with_subtotals:
            assert len(rows) - 1 == len(expect)
        else:
            assert len(rows) + 1 == len(expect)  # +1 for the header row

        self.check_headers(self.get_header_row(), expect[0], assert_matches)

        for idx, expected_row in enumerate(expect[1:]):
            row = rows.eq(idx).find('td')

            try:
                self.check_row(row, expected_row, assert_matches, expect[0])
            except AssertionError as e:
                raise AssertionError(str(e) % idx)

    def assert_grid_count(self, expect):
        assert self.grid.record_count == expect

    def __getitem__(self, item):
        row, col = item
        return self.td(row, col).text().strip()

    def td(self, row, col):
        return self.pyq.find('table.records tbody tr').eq(row)('td').eq(col)

    def csv(self, as_dict=False):
        bytes_data = self.grid.csv.build_csv()
        bytes_data.seek(0)
        csv_data = io.TextIOWrapper(bytes_data)
        reader = csv.DictReader(csv_data) if as_dict else csv.reader(csv_data)

        return [row for row in reader]


class FormBase:
    form_cls = None

    def ok_data(self, **kwargs):
        return kwargs

    def test_disallowed_fields_not_present(self):
        form = self.create_form()
        assert "created_utc" not in form
        assert "updated_utc" not in form

    def test_ok_data_valid(self):
        self.assert_valid()

    def create_form(self, obj=None, **kwargs):
        data = self.ok_data(**kwargs)

        return self.form_cls(MultiDict(data), obj=obj)

    def assert_invalid(self, **kwargs):
        form = self.create_form(**kwargs)
        assert not form.validate(), "expected form errors"
        return form

    def assert_valid(self, **kwargs):
        form = self.create_form(**kwargs)
        assert form.validate(), form.errors
        return form

    def verify_field(
        self, name, label=None, required=False, choice_values=None, prefix=None, suffix=None
    ):
        if required is not None:
            data = {name: ""}
            form = self.create_form(**data)
            field = form[name]
            form.validate()

            if required:
                assert "This field is required." in field.errors
            else:
                assert not field.errors, field.errors
        else:
            form = self.create_form()
            field = form[name]

        if hasattr(field, "choices"):
            if choice_values:
                for index, choice in enumerate(field.iter_choices()):
                    assert index < len(
                        choice_values
                    ), "Too few choice_values.  Field choices: {}".format(field.concrete_choices)
                    assert choice_values[index] == choice[0]
        if label:
            assert field.label.text == label

        if prefix or suffix:
            form = self.create_form()
            field = form[name]

            pq = PyQuery(field())
            if prefix:
                assert pq(".input-group-prepend").text() == prefix
            if suffix:
                assert pq(".input-group-append").text() == suffix
