from django.urls import path # import path, similar toproject's urls.py
from . import views # import views.py from the current directory

urlpatterns = [
    path('', views.index, name='index'),
    path('', include("app_name_urls"),
    name="app_name_urls"), # the app urls are loaded asthe main urls
    ]
