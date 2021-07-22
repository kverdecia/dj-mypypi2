# -*- coding: utf-8 -*-
"Application urls"
from django.urls import path

from . import views


app_name = 'djmypypi2'
urlpatterns = [
    path('', views.PackageListView.as_view(), name='package-list'),
    path('@download/<archive_name>', views.download_package, name='download-package'),
    path('@upload/', views.upload_package, name='upload-package'),
    path('<package_name>/', views.PackageDetailView.as_view(), name='package-detail'),
]
