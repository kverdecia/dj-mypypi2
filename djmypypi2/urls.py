# -*- coding: utf-8 -*-
"Application urls"
from django.urls import path

from . import views


app_name = 'djmypypi2'
urlpatterns = [
    path('', views.PackageListView.as_view(), name='package-list'),
    path('<package_name>/', views.PackageDetailView.as_view(), name='package-detail'),
]
