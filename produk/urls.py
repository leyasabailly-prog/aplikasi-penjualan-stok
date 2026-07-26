from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_produk, name='daftar_produk'),
    path('tambah/', views.tambah_produk, name='tambah_produk'),
    path('edit/<int:produk_id>/', views.edit_produk, name='edit_produk'),
    path('toggle-status/<int:produk_id>/', views.toggle_status_produk, name='toggle_status_produk'),
    path('stok-masuk/', views.form_stok_masuk, name='form_stok_masuk'),
]