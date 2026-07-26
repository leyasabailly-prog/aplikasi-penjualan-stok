from django.contrib import admin
from .models import Penjualan, DetailPenjualan, Retur

class DetailPenjualanInline(admin.TabularInline):
    model = DetailPenjualan
    extra = 1

@admin.register(Penjualan)
class PenjualanAdmin(admin.ModelAdmin):
    list_display = ('no_transaksi', 'kasir', 'total_harga', 'metode_bayar', 'status', 'tanggal')
    list_filter = ('metode_bayar', 'status', 'tanggal')
    search_fields = ('no_transaksi', 'kasir__username')
    inlines = [DetailPenjualanInline]

@admin.register(DetailPenjualan)
class DetailPenjualanAdmin(admin.ModelAdmin):
    list_display = ('penjualan', 'produk', 'qty', 'harga_satuan', 'subtotal')
    search_fields = ('produk__nama_produk', 'penjualan__no_transaksi')

@admin.register(Retur)
class ReturAdmin(admin.ModelAdmin):
    list_display = ('penjualan', 'produk', 'jumlah', 'alasan', 'diproses_oleh', 'tanggal')
    list_filter = ('alasan', 'tanggal')
    search_fields = ('produk__nama_produk', 'penjualan__no_transaksi')

# Register your models here.
