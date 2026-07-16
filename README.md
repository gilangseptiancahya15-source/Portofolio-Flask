# 🚀 Web Portofolio Dinamis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

> Proyek ini dibangun untuk memenuhi **Tugas Capstone Mata Kuliah Pengantar Pemrograman**.

---

## 📖 Deskripsi Singkat

**Web Portofolio Dinamis** adalah sebuah aplikasi web yang dirancang untuk menampilkan karya, keahlian, dan informasi profil secara profesional dan elegan. Dibangun menggunakan framework **Python Flask**, website ini memiliki fitur _Content Management System (CMS)_ minimalis di mana pemilik portofolio (Admin) dapat masuk ke *dashboard* untuk mengelola proyek, keahlian, pengaturan profil, hingga mengelola pesan yang masuk dari pengunjung secara *real-time* tanpa harus mengubah kode pemrograman.

---

## ✨ Fitur Utama Aplikasi

- 🏠 **Halaman Beranda**: Menampilkan ringkasan profil, *quick links*, dan daftar proyek terbaru.
- 🧑‍💻 **Halaman Tentang**: Penjelasan detail mengenai profil, pengalaman, serta daftar keahlian (Skills) yang divisualisasikan dengan rapi.
- 💼 **Halaman Portofolio**: Galeri proyek atau karya yang pernah dibangun.
- 🔍 **Detail Proyek**: Halaman spesifik untuk setiap proyek yang menampilkan deskripsi lengkap, teknologi yang digunakan, serta tautan repositori GitHub dan tautan *live demo*.
- 📞 **Halaman Kontak**: Formulir bagi pengunjung untuk mengirim pesan secara langsung ke pemilik portofolio.
- 🔒 **Login Admin**: Autentikasi aman untuk masuk ke halaman manajemen (Dashboard).
- 🎛️ **Dashboard Admin**: Ringkasan data (total proyek, keahlian, pesan belum terbaca) beserta aksi cepat (*quick actions*).
- 📝 **CRUD Proyek**: Membuat (*Create*), Membaca (*Read*), Mengubah (*Update*), dan Menghapus (*Delete*) data proyek portofolio.
- 🖼️ **Upload Gambar**: Mendukung pengunggahan gambar profil dan _cover_ proyek dengan format yang divalidasi dengan aman.
- ⚙️ **Manajemen Profil & Keahlian**: Mengatur bio, identitas diri, tautan sosial media, menambahkan serta menghapus daftar keahlian teknologi.
- 🛡️ **Ubah Username & Password Admin**: Fitur untuk mengubah kredensial admin secara aman melalui dashboard (dilengkapi validasi sandi lama dan *hashing* otomatis).
- 📨 **Manajemen Pesan Pengunjung**: Melihat status pesan, serta menghapus pesan masuk dari pengunjung.

---

## 🛠️ Teknologi yang Digunakan

| Kategori | Teknologi / Alat |
| :--- | :--- |
| **Backend Framework** | Python, Flask |
| **Database & ORM** | SQLite, Flask-SQLAlchemy |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Styling & UI** | Bootstrap 5, Bootstrap Icons |
| **Template Engine** | Jinja2 |
| **Security & Utilities** | Werkzeug Security (Password Hashing) |

---

## 📁 Struktur Folder Project

```text
portfolio-flask/
├── app.py                  # Entry point & routing logika aplikasi Flask utama
├── config.py               # Konfigurasi aplikasi (Secret Key, Upload Folder, Allowed Extensions)
├── models.py               # Definisi skema tabel Database SQLite (SQLAlchemy ORM)
├── database.db             # File database SQLite (ter-generate otomatis jika belum ada)
├── requirements.txt        # Daftar library/dependensi Python yang dibutuhkan
├── static/                 # Folder aset statis (Frontend)
│   ├── css/                
│   │   └── style.css       # Custom styling CSS (Dark Luxury Theme)
│   ├── js/
│   │   └── main.js         # Interaktivitas JavaScript (Auto-dismiss alert, Tooltips, dll)
│   └── uploads/            # Direktori penyimpanan gambar yang di-upload
└── templates/              # Folder file Jinja2 HTML templates
    ├── base.html           # Layout utama (navbar, footer, styling dasar, flash messages)
    ├── index.html          # Halaman Beranda (Home)
    ├── about.html          # Halaman Tentang
    ├── portfolio.html      # Halaman Daftar Portofolio
    ├── project_detail.html # Halaman Detail Proyek tunggal
    ├── contact.html        # Halaman Kontak
    └── dashboard/          # Folder template untuk area Admin (Dilindungi login)
        ├── account.html    # Halaman pengaturan kredensial (Username & Password)
        ├── add_project.html# Form tambah proyek baru
        ├── edit_project.html# Form edit informasi proyek
        ├── index.html      # Halaman Utama Dashboard (Ringkasan statistik)
        ├── login.html      # Halaman Autentikasi Login (Mewarisi base.html)
        ├── messages.html   # Halaman Kotak Masuk (Pesan)
        ├── profile.html    # Halaman Kelola Profil & Skill
        └── projects.html   # Halaman Kelola Daftar Proyek
```

---

## 🚀 Cara Instalasi & Menjalankan Project

Ikuti langkah-langkah berikut untuk menjalankan aplikasi web ini di komputer lokal Anda:

### 1. Clone Repository
Buka terminal / *command prompt* dan jalankan perintah:
```bash
git clone <URL GitHub>
cd portfolio-flask
```

### 2. Membuat Virtual Environment (Sangat Disarankan)
Untuk mengisolasi *library* proyek ini dari sistem utama komputer Anda:
**Bagi Pengguna Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**Bagi Pengguna macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements
Setelah virtual environment dipastikan aktif, instal semua dependensi yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi
Jalankan file utama web server Flask:
```bash
python app.py
```
Website portofolio dapat langsung diakses melalui browser pada alamat URL: **`http://127.0.0.1:5000`**

---

## 🗄️ Konfigurasi Database SQLite

Aplikasi ini menggunakan sistem database yang sangat praktis (SQLite).
- File database **`database.db`** akan **terbuat secara otomatis** saat pertama kali aplikasi (`app.py`) dijalankan. 
- Anda tidak perlu mengonfigurasi *server* database apapun secara eksternal. Struktur tabel akan menyesuaikan dengan model yang ada.

---

## 🔐 Akun Login Admin (Default)

Saat pertama kali dijalankan (jika database masih kosong), sistem akan otomatis membuat satu akun admin *default* untuk Anda masuk ke *Dashboard*.

- **URL Akses Login:** `http://127.0.0.1:5000/dashboard/login`
- **Username:** `admin`
- **Password:** `admin123`

> **⚠️ PENTING:** Segera setelah Anda berhasil _login_, harap langsung mengubah _Username_ dan _Password_ ini melalui menu **Pengaturan Akun** di _Dashboard_ untuk menjaga keamanan web portofolio Anda!

---

## 📦 Daftar Library yang Digunakan

Proyek ini sangat bergantung pada library-library Python berikut (silakan merujuk pada `requirements.txt`):
- **`Flask`** (Kerangka/Framework web backend)
- **`Flask-SQLAlchemy`** (Sistem ORM untuk kemudahan kueri ke Database)
- **`Werkzeug`** (Utilitas pengamanan/hashing *password* dan sanitasi *upload* file)

---

## 📝 Lisensi

Proyek ini dibuat, diimplementasikan, dan diserahkan untuk keperluan penyelesaian tugas *Capstone* dan *showcase* akademik.

---

## 👨‍🎓 Identitas Pengembang

- **Nama Lengkap:** `<Gilang Septian Cahya Saputra>`
- **Nomor Induk Mahasiswa (NIM):** `<301250022>`
- **Universitas:** `<Universitas Bale Bandung>`
- **Program Studi:** `<Teknik Informatika>`
