from django.urls import path # import path, similar toproject's urls.py
from . import views # import views.py from the current directory

urlpatterns = [
    path('', views.index, name='index'),
    ]
