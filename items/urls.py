from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'items'
urlpatterns = [
    path('<int:item_pk>/', views.item_detail, name='item_detail'),
    path('create/', views.item_create, name='item_create'),
    path('<int:item_pk>/edit/', views.item_update, name='item_update'),
    path('<int:item_pk>/delete/', views.item_delete, name='item_delete'),
    path('<int:item_pk>/copy/', views.item_copy, name='item_copy'),
    path('delete/', login_required(views.ItemsDelete.as_view()), name='items_delete'),
    path('export/', login_required(views.ItemExport.as_view()), name='item_export'),
    path('import/', login_required(views.ItemImport.as_view()), name='item_import'),
    path('', views.item_detail, name='item_detail'),
]