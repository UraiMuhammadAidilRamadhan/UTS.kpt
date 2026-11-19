# Sistem Kasir dan Manajemen Stok UMKM

**Video presentasi:** isi tautan YouTube Unlisted di sini setelah video selesai dibuat.

REST API untuk mengelola produk, stok, dan transaksi UMKM menggunakan FastAPI, SQLite, dan aiosqlite.

## Fitur
- CRUD produk pada `/resource`
- Pembuatan dan pemantauan transaksi pada `/transactions`
- Pemrosesan background dengan status pending, processing, completed, atau failed
- Penguncian stok menggunakan `asyncio.Lock`
- Skrip seed, uji race condition, dan Locust

## Persyaratan
Python 3.10 atau lebih baru.

## Instalasi Windows PowerShell
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload --port 8000
```

Buka Swagger UI: http://127.0.0.1:8000/docs

## Pengujian race condition
Atur stok produk ID 1 menjadi 1 melalui `PUT /resource/1`.

Jalankan server satu worker dengan Lock aktif:
```powershell
$env:STOCK_LOCK_ENABLED="true"
uvicorn main:app --port 8000
```
Di terminal kedua:
```powershell
.\venv\Scripts\Activate.ps1
python test_race.py
```
Hasil yang diharapkan: satu request diterima dan request lainnya mendapat HTTP 409.

Untuk demonstrasi tanpa Lock, hentikan server lalu jalankan:
```powershell
$env:STOCK_LOCK_ENABLED="false"
uvicorn main:app --port 8000
```
Reset stok produk ID 1 menjadi 1 sebelum menjalankan `python test_race.py` lagi. Pada kondisi tanpa Lock, dua request dapat sama-sama membaca stok awal 1 dan keduanya diterima. Karena kedua update dapat menulis nilai stok yang sama, contoh ini dapat menunjukkan overselling pada jumlah transaksi, tetapi nilai stok akhir dapat menjadi 0 (lost update), bukan selalu negatif. Jika dosen mensyaratkan stok akhir negatif, implementasi decrement SQL dan desain uji perlu disesuaikan agar kedua decrement diterapkan.

## Benchmark Locust
Jalankan server dengan satu worker:
```powershell
uvicorn main:app --workers 1 --port 8000
```
Jalankan Locust dari terminal lain:
```powershell
locust -f locustfile.py --host http://127.0.0.1:8000
```
Buka http://localhost:8089. Uji skenario read: 100 users/request sesuai pengaturan dosen (20 spawn rate), dan skenario write: 50 request dengan concurrency 10. Catat hasil aktual untuk dibandingkan dengan 4 worker.

Hentikan server, lalu jalankan:
```powershell
uvicorn main:app --workers 4 --port 8000
```
Ulangi pengujian dengan kondisi dan data yang sebanding. Jangan mengarang angka benchmark; masukkan hasil pengujian nyata ke laporan.

## Endpoint
| Method | Path | Fungsi |
|---|---|---|
| GET | `/resource?skip=0&limit=10` | Daftar produk |
| GET | `/resource/{id}` | Detail produk |
| POST | `/resource` | Tambah produk |
| PUT | `/resource/{id}` | Ubah produk |
| DELETE | `/resource/{id}` | Hapus produk |
| POST | `/transactions` | Buat transaksi |
| GET | `/transactions` | Daftar transaksi, opsional `?status=pending` |
| GET | `/transactions/{id}` | Detail transaksi |

## Catatan teknis
`asyncio.Lock` hanya melindungi coroutine dalam satu proses worker. Lock Python ini tidak dibagi antar proses Uvicorn. Untuk pengujian multi-worker yang benar-benar aman terhadap stok, diperlukan penguncian/transaksi di tingkat database. Untuk demonstrasi B3 sesuai instruksi, gunakan satu worker.
