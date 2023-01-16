import datetime as dt
import decimal
import json

import arrow
import flask.json


class JSONProvider(flask.json.provider.DefaultJSONProvider):
    """
    The Flask JSON provider but puts dates in iso format instead of http date format,
    and converts float to decimal during parse.
    """

    def default(self, obj):
        if isinstance(obj, (dt.datetime, dt.date, arrow.Arrow)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super().default(obj)

    def loads(self, s, **kwargs):
        # Same as simplejson.loads(..., use_decimal=True)
        kwargs.setdefault('parse_float', decimal.Decimal)
        # Don't call super here (may get request object issues from code setting up
        # deprecation warning)
        return json.loads(s, **kwargs)
