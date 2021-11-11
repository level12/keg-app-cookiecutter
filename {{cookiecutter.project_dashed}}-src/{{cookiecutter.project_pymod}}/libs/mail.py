from collections import namedtuple

from blazeutils.strings import normalizews
import flask
from . import markdown

MailParts = namedtuple('MailParts', 'subject text html')


def mail_template(template_name_or_list, **kwargs):
    multi_part_content = flask.render_template(template_name_or_list, **kwargs)
    parts = multi_part_content.split('---multi-part:xFE+Ab7j+w,mdIL%---')
    subject, markdown = map(lambda p: p.strip(), parts)

    return MailParts(
        normalizews(subject),
        markdown,
        markdown.render(markdown)
    )
