from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from produk.models import Produk
from .models import Penjualan, DetailPenjualan


@login_required
@role_required( 'kasir')
def buat_transaksi(request):
    keranjang = request.session.get('keranjang', {})

    if request.method == 'POST':
        produk_id = request.POST.get('produk_id')
        qty = int(request.POST.get('qty', 0))
        produk = get_object_or_404(Produk, id=produk_id)

        if qty <= 0:
            messages.error(request, 'Jumlah harus lebih dari 0.')
        else:
            qty_sekarang = keranjang.get(str(produk_id), 0)
            if qty_sekarang + qty > produk.stok:
                messages.error(request, f'Stok {produk.nama_produk} tidak cukup. Sisa stok: {produk.stok}')
            else:
                keranjang[str(produk_id)] = qty_sekarang + qty
                request.session['keranjang'] = keranjang
                messages.success(request, f'{produk.nama_produk} ditambahkan ke keranjang.')

        return redirect('buat_transaksi')

    produk_list = Produk.objects.filter(is_active=True)

    items = []
    total = 0
    for produk_id, qty in keranjang.items():
        produk = Produk.objects.filter(id=produk_id).first()
        if produk:
            subtotal = produk.harga_jual * qty
            total += subtotal
            items.append({'produk': produk, 'qty': qty, 'subtotal': subtotal})

    context = {
        'produk_list': produk_list,
        'items': items,
        'total': total,
    }
    return render(request, 'transaksi/buat_transaksi.html', context)


@login_required
@role_required( 'kasir')
def hapus_item(request, produk_id):
    keranjang = request.session.get('keranjang', {})
    keranjang.pop(str(produk_id), None)
    request.session['keranjang'] = keranjang
    return redirect('buat_transaksi')


@login_required
@role_required('kasir')
def checkout(request):
    keranjang = request.session.get('keranjang', {})

    if not keranjang:
        messages.error(request, 'Keranjang masih kosong.')
        return redirect('buat_transaksi')

    penjualan = Penjualan.objects.create(kasir=request.user)

    for produk_id, qty in keranjang.items():
        produk = get_object_or_404(Produk, id=produk_id)

        if qty > produk.stok:
            messages.error(request, f'Stok {produk.nama_produk} tidak cukup saat checkout.')
            penjualan.delete()
            return redirect('buat_transaksi')

        detail = DetailPenjualan(
            penjualan=penjualan,
            produk=produk,
            qty=qty,
            harga_satuan=produk.harga_jual,
            subtotal=produk.harga_jual * qty,
        )
        detail.save()

    penjualan.total_harga = sum(d.subtotal for d in penjualan.detail.all())
    penjualan.save()

    request.session['keranjang'] = {}

    return redirect('struk_transaksi', penjualan_id=penjualan.id)


@login_required
def struk(request, penjualan_id):
    penjualan = get_object_or_404(Penjualan, id=penjualan_id)
    return render(request, 'transaksi/struk.html', {'penjualan': penjualan})

@login_required
@role_required('admin' , 'kasir')
def riwayat_transaksi(request):
    penjualan_list = Penjualan.objects.all().order_by('-tanggal')
    return render(request, 'transaksi/riwayat_transaksi.html', {'penjualan_list': penjualan_list})
# Create your views here.
