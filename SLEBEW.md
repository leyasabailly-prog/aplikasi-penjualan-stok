🛒 Aplikasi Penjualan & Stok
Aplikasi berbasis web untuk membantu usaha kecil-menengah mengelola penjualan (kasir/POS) dan stok barang dalam satu sistem. Aplikasi ini mendukung banyak pengguna dengan peran berbeda (Admin/Owner, Kasir, dan Staff Gudang), sehingga setiap pengguna hanya bisa mengakses fitur sesuai tanggung jawabnya.
Dengan aplikasi ini, pemilik usaha dapat memantau transaksi harian, tren penjualan, kondisi stok (aman/menipis/habis), serta mengelola data produk, kategori, dan supplier secara terpusat.
👥 Anggota Kelompok
No.
NIM
Nama
1. 2421400081
Faneshya Sakila Fitri
2. 2421400154
Lailatul Mufarrohah
3. 2421400069
Risqi Wulandari
4. 2421400059
Ulfa Lailatul Khusnia
🧩 Pembagian Tugas
Anggota
Tugas
**Risqi Wulandari**
Perancangan database & model (Profile, Kategori, Supplier, Produk, StokMasuk, Penjualan, dll), backend modul autentikasi & role
**Faneshya Sakila Fitri**
Pengembangan modul Produk & Stok (tambah/edit produk, stok masuk, kategori, supplier)
**Lailatul Mufarrohah**
Pengembangan modul Transaksi (buat transaksi, checkout, struk, riwayat, retur)
**Ulfa Lailatul Khusnia**
Pengembangan modul Dashboard (ringkasan penjualan, grafik tren, status stok) & tampilan (UI/UX)
Catatan: pembagian tugas di atas adalah rangkuman umum berdasarkan modul yang dikerjakan; silakan sesuaikan kembali sesuai kontribusi aktual masing-masing anggota.
✨ Fitur
🔐 Autentikasi & Role Pengguna
Login & logout
3 peran pengguna: Admin/Owner, Kasir, Staff Gudang
Pembatasan akses halaman berdasarkan peran (role-based access control)
📊 Dashboard
Ringkasan total penjualan hari ini & perbandingan dengan hari kemarin
Grafik tren penjualan 7 hari terakhir
Status stok produk (aman / menipis / habis)
Daftar produk terlaris (7 hari terakhir)
Aktivitas terbaru (transaksi & stok masuk)
📦 Manajemen Produk & Stok
CRUD data produk (kode, nama, kategori, supplier, harga beli, harga jual, satuan, gambar)
Manajemen kategori produk
Manajemen data supplier
Pencatatan stok masuk (stok otomatis bertambah)
Aktif/nonaktifkan produk
Validasi harga jual tidak boleh lebih rendah dari harga beli
Notifikasi stok menipis berdasarkan stok minimum
💳 Transaksi Penjualan
Membuat transaksi penjualan baru
Checkout dengan metode pembayaran (Tunai, Transfer, QRIS)
Nomor transaksi otomatis (format TRX-XXXXXXXX)
Stok otomatis berkurang saat produk terjual
Cetak struk transaksi
Riwayat transaksi
Retur barang (stok otomatis dikembalikan)
Validasi stok agar tidak menjual melebihi stok tersedia
🛠 Teknologi yang Digunakan
Bahasa Pemrograman: Python 3.13
Framework: Django 6.0
Database: SQLite
Frontend: Django Template + HTML, CSS
Library tambahan:
Pillow (pengolahan gambar produk)
asgiref, sqlparse, tzdata (dependensi bawaan Django)
⚙️ Cara Instalasi
Clone repository
git clone https://github.com/leyasabailly-prog/aplikasi-penjualan-stok.git
cd aplikasi-penjualan-stok
Buat virtual environment
python -m venv venv
Aktifkan virtual environment
Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate
Install dependencies
pip install -r requirements.txt
Jalankan migrasi database
python manage.py migrate
(Opsional) Buat superuser
python manage.py createsuperuser
▶️ Cara Menjalankan Aplikasi
Jalankan server pengembangan Django:
python manage.py runserver
Buka browser dan akses:
http://127.0.0.1:8000/
Login menggunakan akun pengujian di bawah, atau akun superuser yang telah dibuat.
🔑 Akun Pengujian
Peran
Username
Password
Admin/Owner
admin
admin123
Kasir
sitti
sitti kasir
Staff Gudang
wulan
wulan123
Catatan: pastikan setiap akun sudah memiliki data Profile dengan role yang sesuai (
admin, kasir, atau gudang) agar sistem pembatasan akses berjalan dengan benar. Role dapat diatur melalui halaman Django Admin (/admin/
).
📁 Struktur Proyek (Ringkas)
aplikasi-penjualan-stok/
├── accounts/       # Autentikasi & role pengguna
├── produk/         # Kategori, supplier, produk, stok masuk
├── transaksi/      # Penjualan, checkout, struk, retur
├── dashboard/      # Ringkasan & statistik
├── core/           # Konfigurasi utama proyek Django
├── templates/      # Template dasar (base.html)
├── manage.py
└── requirements.txt
