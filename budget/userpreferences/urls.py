from . import views
from django.urls import path


urlpatterns=[
    path('', views.index, name="preferences"),
    path('category-delete/<int:id>', views.delete_category, name='category-delete'),
    path('edit-category/<int:id>', views.edit_category, name='category-edit'),
    path('add-category', views.add_category, name='category-add'),
    path('budynek-delete/<int:id>', views.delete_budynek, name='budynek-delete'),
    path('edit-budynek/<int:id>', views.edit_budynek, name='budynek-edit'),
    path('add-budynek', views.add_budynek, name='budynek-add'),
    path('source-delete/<int:id>', views.delete_source, name='source-delete'),
    path('edit-source/<int:id>', views.edit_source, name='source-edit'),
    path('add-source', views.add_source, name='source-add'),




]