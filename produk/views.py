from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Produk, StokMasuk
from .forms import ProdukForm


@login_required
def daftar_produk(request):
    produk_list = Produk.objects.all()
    return render(request, 'produk/daftar_produk.html', {'produk_list': produk_list})


@login_required
@role_required('admin', 'gudang')
def tambah_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST, request.FILES)
        if form.is_valid():
            produk = form.save(commit=False)
            produk.is_active = True
            produk.save()
            messages.success(request, f'Produk "{produk.nama_produk}" berhasil ditambahkan.')
            return redirect('daftar_produk')    
        else:
            messages.error(request, 'Data belum valid, cek kembali form-nya.')
    else:
        form = ProdukForm()

    return render(request, 'produk/form_produk.html', {'form': form})

from django.shortcuts import get_object_or_404


@login_required
@role_required('admin', 'gudang')
def edit_produk(request, produk_id):
    produk = get_object_or_404(Produk, id=produk_id)

    if request.method == 'POST':
        form = ProdukForm(request.POST, request.FILES, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produk "{produk.nama_produk}" berhasil diperbarui.')
            return redirect('daftar_produk')
        else:
            messages.error(request, 'Data belum valid, cek kembali form-nya.')
    else:
        form = ProdukForm(instance=produk)

    return render(request, 'produk/form_produk.html', {'form': form, 'mode': 'edit', 'produk': produk})

@login_required
@role_required('admin', 'gudang')
def toggle_status_produk(request, produk_id):
    produk = get_object_or_404(Produk, id=produk_id)

    if request.method == 'POST':
        produk.is_active = not produk.is_active
        produk.save()
        status_text = 'diaktifkan' if produk.is_active else 'dinonaktifkan'
        messages.success(request, f'Produk "{produk.nama_produk}" berhasil {status_text}.')
        return redirect('daftar_produk')

    return render(request, 'produk/konfirmasi_status.html', {'produk': produk})

@login_required
@role_required('admin', 'gudang')
def form_stok_masuk(request):
    if request.method == 'POST':
        produk_id = request.POST.get('produk_id')
        jumlah = int(request.POST.get('jumlah', 0))
        keterangan = request.POST.get('keterangan', '')
        produk = Produk.objects.filter(id=produk_id).first()

        if not produk or jumlah <= 0:
            messages.error(request, 'Produk atau jumlah tidak valid.')
        else:
            StokMasuk.objects.create(
                produk=produk,
                jumlah=jumlah,
                harga_beli_saat_ini=produk.harga_beli,
                user=request.user,
                keterangan=keterangan,
            )
            messages.success(request, f'Stok {produk.nama_produk} berhasil ditambahkan sebanyak {jumlah}.')

        return redirect('form_stok_masuk')

    produk_list = Produk.objects.filter(is_active=True)
    riwayat = StokMasuk.objects.all().order_by('-tanggal')[:20]
    return render(request, 'produk/stok_masuk.html', {'produk_list': produk_list, 'riwayat': riwayat})