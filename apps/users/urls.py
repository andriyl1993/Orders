from django.conf.urls import url
from views import login_ctrl, signup_ctrl, logout_ctrl, forgot_ctrl, restore_pass_ctrl

urlpatterns = [
    url(r'login/', login_ctrl, name='login'),
    url(r'logout/', logout_ctrl, name='logout'),
    url(r'sign-up/', signup_ctrl, name='sign_up'),
    url(r'forgot/', forgot_ctrl, name='forgot'),
    url(r'restore/', restore_pass_ctrl, name='restore'),
]