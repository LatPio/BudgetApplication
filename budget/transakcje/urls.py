from . import views
from django.urls import path


urlpatterns=[
    path('transakcje/', views.index, name="transakcje"),





]