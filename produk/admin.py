from django.contrib import admin
from .models import Kategori, Supplier, Produk, StokMasuk

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama_kategori', 'created_at')
    search_fields = ('nama_kategori',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('nama_supplier', 'kontak', 'email', 'created_at')
    search_fields = ('nama_supplier', 'kontak')

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('kode_produk', 'nama_produk', 'kategori', 'supplier', 'harga_beli', 'harga_jual', 'stok', 'is_low_stock', 'is_active')
    list_filter = ('kategori', 'supplier', 'is_active')
    search_fields = ('kode_produk', 'nama_produk')

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Stok Menipis'

@admin.register(StokMasuk)
class StokMasukAdmin(admin.ModelAdmin):
    list_display = ('produk', 'jumlah', 'harga_beli_saat_ini', 'user', 'tanggal')
    list_filter = ('tanggal',)
    search_fields = ('produk__nama_produk',)

# Register your models here.
