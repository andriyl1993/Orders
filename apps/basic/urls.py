from django.conf.urls import url, include
from django.contrib import admin
from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index')
]