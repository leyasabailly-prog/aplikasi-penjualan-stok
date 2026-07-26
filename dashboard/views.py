from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
from produk.models import Produk, StokMasuk
from transaksi.models import Penjualan, DetailPenjualan


@login_required
def dashboard_view(request):
    today = timezone.localdate()
    start_7 = today - timedelta(days=6)

    total_hari_ini = Penjualan.objects.filter(
        tanggal__date=today, status='selesai'
    ).aggregate(t=Sum('total_harga'))['t'] or 0

    kemarin = today - timedelta(days=1)
    total_kemarin = Penjualan.objects.filter(
        tanggal__date=kemarin, status='selesai'
    ).aggregate(t=Sum('total_harga'))['t'] or 0

    if total_kemarin > 0:
        persen_perubahan = round(((total_hari_ini - total_kemarin) / total_kemarin) * 100, 1)
    else:
        persen_perubahan = 0

    tren_label = []
    tren_data = []
    for i in range(6, -1, -1):
        tgl = today - timedelta(days=i)
        total = Penjualan.objects.filter(
            tanggal__date=tgl, status='selesai'
        ).aggregate(t=Sum('total_harga'))['t'] or 0
        tren_label.append(tgl.strftime('%d/%m'))
        tren_data.append(float(total))

    produk_qs = Produk.objects.filter(is_active=True)
    stok_aman = produk_qs.filter(stok__gt=F('stok_minimum')).count()
    stok_menipis = produk_qs.filter(stok__gt=0, stok__lte=F('stok_minimum')).count()
    stok_habis = produk_qs.filter(stok=0).count()
    total_produk = produk_qs.count() or 1

    terlaris_qs = (
        DetailPenjualan.objects
        .filter(penjualan__tanggal__date__gte=start_7, penjualan__status='selesai')
        .values('produk__nama_produk')
        .annotate(total_qty=Sum('qty'))
        .order_by('-total_qty')[:5]
    )
    terlaris = list(terlaris_qs)
    max_qty = max([t['total_qty'] for t in terlaris], default=1)

    penjualan_terbaru = Penjualan.objects.filter(status='selesai').order_by('-tanggal')[:4]
    stok_masuk_terbaru = StokMasuk.objects.order_by('-tanggal')[:4]

    aktivitas = []
    for p in penjualan_terbaru:
        aktivitas.append({
            'jenis': 'transaksi',
            'waktu': p.tanggal,
            'teks': f'Transaksi {p.no_transaksi}',
            'sub': f'Rp{p.total_harga:,.0f} · {p.kasir}'.replace(',', '.'),
        })
    for s in stok_masuk_terbaru:
        aktivitas.append({
            'jenis': 'stok',
            'waktu': s.tanggal,
            'teks': f'Stok masuk · {s.produk.nama_produk}',
            'sub': f'+{s.jumlah} pcs',
        })
    aktivitas.sort(key=lambda x: x['waktu'], reverse=True)
    aktivitas = aktivitas[:6]

    context = {
        'hari_ini': today,
        'total_hari_ini': total_hari_ini,
        'persen_perubahan': persen_perubahan,
        'tren_label': tren_label,
        'tren_data': tren_data,
        'stok_aman': stok_aman,
        'stok_menipis': stok_menipis,
        'stok_habis': stok_habis,
        'total_produk': total_produk,
        'terlaris': terlaris,
        'max_qty': max_qty,
        'aktivitas': aktivitas,
    }
    return render(request, 'dashboard/dashboard.html', context)