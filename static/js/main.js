/**
 * Main JavaScript File untuk Portfolio
 * Berisi interaksi UI, animasi, dan fungsi pendukung lainnya.
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Auto-dismiss Flash Messages
    // Menghilangkan pesan notifikasi (flash) secara otomatis setelah 5 detik
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(alert => {
                // Menggunakan class Bootstrap untuk menutup alert dengan animasi
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 5000); // 5000 ms = 5 detik
    }

    // 2. Inisialisasi Bootstrap Tooltips & Popovers
    // Mengaktifkan fitur tooltip (teks bantuan kecil saat di-hover) jika digunakan
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 3. Efek Shadow pada Navbar saat di-scroll
    // Membuat navbar sedikit transparan di awal, lalu memunculkan shadow saat di-scroll ke bawah
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow-sm');
                // Anda bisa menambahkan class transisi atau merubah warna background disini jika diperlukan
            } else {
                navbar.classList.remove('shadow-sm');
            }
        });
    }

    // 4. Smooth Scrolling untuk link internal (Anchor Links)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

});
