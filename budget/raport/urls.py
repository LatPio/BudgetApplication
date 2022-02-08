from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('raport/', views.index, name="raport"),

    path('excel_preaty_raport/<rok>', views.excel_preaty_raport, name='excel_preaty_raport'),
    path('export-excel', views.export_excel, name='export-excel')



]

