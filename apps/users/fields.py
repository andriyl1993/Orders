from __future__ import unicode_literals

import re

from django.db import models


class PhoneField(models.CharField):
    description = "Phone field +xx(xxx)xxx-xx-xx"

    _field_regex = r"(\d{2})\((\d{3})\)(\d{3})-(\d{2})-(\d{2})$"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12
        super(PhoneField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(PhoneField, self).deconstruct()
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        return '+' + value[:2] + '(' + value[2:5] + ')' + value[5:8] + '-' + value[8:10] + '-' + value[10:]

    def _from_display_to_save(self, value):
        regular = re.compile(self._field_regex)
        if value:
            arr = regular.search(value).groups()
            return "".join(arr)
        else:
            return ''

    def get_prep_value(self, value, *args, **kwargs):
        return self._from_display_to_save(value)

    def to_python(self, value):
        return self._from_display_to_save(value)

    def get_internal_type(self):
        return 'CharField'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value
