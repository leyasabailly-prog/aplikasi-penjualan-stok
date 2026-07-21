from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from produk.models import Produk
import uuid


class Penjualan(models.Model):
    METODE_BAYAR = [
        ('tunai', 'Tunai'),
        ('transfer', 'Transfer'),
        ('qris', 'QRIS'),
    ]
    STATUS_CHOICES = [
        ('selesai', 'Selesai'),
        ('dibatalkan', 'Dibatalkan'),
    ]

    no_transaksi = models.CharField(max_length=20, unique=True, blank=True)
    kasir = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transaksi_penjualan')
    total_harga = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    metode_bayar = models.CharField(max_length=10, choices=METODE_BAYAR, default='tunai')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='selesai')
    tanggal = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.no_transaksi:
            self.no_transaksi = f"TRX-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.no_transaksi

    class Meta:
        ordering = ['-tanggal']
        verbose_name = "Penjualan"
        verbose_name_plural = "Penjualan"


class DetailPenjualan(models.Model):
    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE, related_name='detail')
    produk = models.ForeignKey(Produk, on_delete=models.PROTECT, related_name='detail_penjualan')
    qty = models.PositiveIntegerField()
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, blank=True)

    def clean(self):
        # Validasi: qty tidak boleh melebihi stok tersedia
        if self.qty > self.produk.stok:
            raise ValidationError(
                f'Stok {self.produk.nama_produk} tidak mencukupi. Sisa stok: {self.produk.stok}'
            )

    def save(self, *args, **kwargs):
        if not self.harga_satuan:
            self.harga_satuan = self.produk.harga_jual
        self.subtotal = self.qty * self.harga_satuan

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Kurangi stok produk otomatis
            self.produk.stok -= self.qty
            self.produk.save()

    def __str__(self):
        return f"{self.produk.nama_produk} x{self.qty}"

    class Meta:
        verbose_name = "Detail Penjualan"
        verbose_name_plural = "Detail Penjualan"


class Retur(models.Model):
    ALASAN_CHOICES = [
        ('rusak', 'Barang Rusak'),
        ('salah_kirim', 'Salah Kirim'),
        ('tidak_sesuai', 'Tidak Sesuai Pesanan'),
        ('lainnya', 'Lainnya'),
    ]

    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE, related_name='retur')
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, related_name='retur')
    jumlah = models.PositiveIntegerField()
    alasan = models.CharField(max_length=15, choices=ALASAN_CHOICES, default='lainnya')
    keterangan = models.TextField(blank=True, null=True)
    diproses_oleh = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='retur_diproses')
    tanggal = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Barang retur dikembalikan ke stok
            self.produk.stok += self.jumlah
            self.produk.save()

    def __str__(self):
        return f"Retur: {self.produk.nama_produk} x{self.jumlah}"

    class Meta:
        ordering = ['-tanggal']
        verbose_name_plural = "Retur"

# Create your models here.
