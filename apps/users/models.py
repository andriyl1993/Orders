from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from fields import PhoneField


class MyUser(User):
    phone = PhoneField()
