from django.urls import path
from . import views

urlpatterns = [
    path('buat/', views.buat_transaksi, name='buat_transaksi'),
    path('hapus/<int:produk_id>/', views.hapus_item, name='hapus_item_transaksi'),
    path('checkout/', views.checkout, name='checkout_transaksi'),
    path('struk/<int:penjualan_id>/', views.struk, name='struk_transaksi'),
    path('riwayat/', views.riwayat_transaksi, name='riwayat_transaksi'),
]