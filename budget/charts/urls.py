from django.urls import path
from . import views


urlpatterns = [
    path('charts/', views.index, name="charts"),
    path('chartYearView/<rok>', views.chartYearView, name="chartYearView"),




]

