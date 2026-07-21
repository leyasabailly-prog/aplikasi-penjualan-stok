from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_kategori

    class Meta:
        verbose_name_plural = "Kategori"
        ordering = ['nama_kategori']


class Supplier(models.Model):
    nama_supplier = models.CharField(max_length=150)
    kontak = models.CharField(max_length=20)
    alamat = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_supplier

    class Meta:
        ordering = ['nama_supplier']


class Produk(models.Model):
    kode_produk = models.CharField(max_length=20, unique=True)
    nama_produk = models.CharField(max_length=150)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, related_name='produk')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='produk')
    harga_beli = models.DecimalField(max_digits=12, decimal_places=2)
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2)
    stok = models.PositiveIntegerField(default=0)
    stok_minimum = models.PositiveIntegerField(default=5)
    satuan = models.CharField(max_length=20, default='pcs')
    gambar = models.ImageField(upload_to='produk/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.harga_jual < self.harga_beli:
            raise ValidationError('Harga jual tidak boleh lebih kecil dari harga beli.')

    @property
    def is_low_stock(self):
        return self.stok <= self.stok_minimum

    def __str__(self):
        return f"{self.kode_produk} - {self.nama_produk}"

    class Meta:
        ordering = ['nama_produk']


class StokMasuk(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, related_name='riwayat_stok_masuk')
    jumlah = models.PositiveIntegerField()
    harga_beli_saat_ini = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='input_stok')
    keterangan = models.CharField(max_length=255, blank=True, null=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Tambahkan stok produk otomatis saat ada stok masuk baru
            self.produk.stok += self.jumlah
            self.produk.save()

    def __str__(self):
        return f"Stok masuk: {self.produk.nama_produk} (+{self.jumlah})"

    class Meta:
        ordering = ['-tanggal']
        verbose_name = "Stok Masuk"
        verbose_name_plural = "Stok Masuk"

# Create your models here.
