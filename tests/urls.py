# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns("",
    url(r"", include('django_tits.urls')),
)