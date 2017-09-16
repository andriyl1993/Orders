import re

from django.core.exceptions import ValidationError
from fields import PhoneField

RESTORE_CODE_MIN_VALUE = 1000000000
RESTORE_CODE_MAX_VALUE = 9999999999

def char(string, min_len=None, max_len=None):
    if min_len is not None and len(string) < min_len or max_len is not None and len(string) > max_len:
        raise ValidationError('String has incorrect length')
    return True

def phone(string):
    try:
        r = re.compile(PhoneField._field_regex)
        res = r.search(string)
    except Exception, e:
        res = False
    if res:
        return True
    raise ValidationError('Phone has incorrect format')

def integer(value, min_val, max_val):
    if value > max_val or value < min_val:
        raise ValidationError('Value have to be in range(%d, %d)' % (min_val, max_val))
    return True
