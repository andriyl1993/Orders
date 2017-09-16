from django import forms
from models import MyUser
from validators import char, phone, integer, RESTORE_CODE_MIN_VALUE, RESTORE_CODE_MAX_VALUE


class MyUserForm(forms.Form):
    username = forms.CharField(validators=[lambda x: char(x, min_len=6, max_len=64)], required=False)
    first_name = forms.CharField(validators=[lambda x: char(x, max_len=64)], required=False)
    last_name = forms.CharField(validators=[lambda x: char(x, max_len=64)], required=False)
    email = forms.EmailField(required=False)
    password = forms.PasswordInput()
    phone = forms.CharField(validators=[phone], required=False)

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone']


class RestorePassword(forms.Form):
    code = forms.IntegerField(validators=[lambda x: integer(x, min_val=RESTORE_CODE_MIN_VALUE, max_val=RESTORE_CODE_MAX_VALUE)])
    password = forms.PasswordInput()
    rep_password = forms.PasswordInput()