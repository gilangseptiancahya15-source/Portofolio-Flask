import os
import uuid
from functools import wraps
from flask import Flask, render_template, request, flash, redirect, url_for, session
from config import Config
from models import db, User, Project, Skill, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

def init_database():
    with app.app_context():
        db.create_all()
        admin = User.query.first()
        if admin is None:
            admin_baru = User(
                username='admin',
                password=generate_password_hash('admin123'),
                name='Gilang Septian',
                email='gilang@example.com',
                bio='Mahasiswa Teknik Informatika yang antusias dalam pengembangan web dan teknologi.',
            )
            db.session.add(admin_baru)

            skill_default = [
                Skill(name='Python', level=80),
                Skill(name='HTML/CSS', level=85),
                Skill(name='JavaScript', level=70),
                Skill(name='Flask', level=75),
                Skill(name='SQL', level=65),
            ]
            db.session.add_all(skill_default)
            db.session.commit()
            print('>> Database berhasil dibuat!')


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/')
def index():
    # Mengambil maksimal 3 project terbaru (berdasarkan id/waktu)
    projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    return render_template('index.html', projects=projects)

@app.route('/about')
def about():
    # Mengambil skill dan diurutkan dari level tertinggi ke terendah
    skills = Skill.query.order_by(Skill.level.desc()).all()
    return render_template('about.html', skills=skills)

@app.route('/portfolio')
def portfolio():
    # Mengambil semua project
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('portfolio.html', projects=projects)

@app.route('/project/<int:id>')
def project_detail(id):
    # Mengambil satu project berdasarkan ID. Jika ID tidak ada, tampilkan error 404
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Jika pengunjung mensubmit form
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        subject = request.form.get('subject', '')
        body = request.form.get('body', '')
        
        # Validasi Input: Pastikan tidak ada spasi kosong saja
        if not name.strip() or not email.strip() or not subject.strip() or not body.strip():
            flash('Semua field wajib diisi dengan benar!', 'danger')
        else:
            # Simpan pesan ke database
            pesan_baru = Message(name=name, email=email, subject=subject, body=body)
            db.session.add(pesan_baru)
            db.session.commit()
            
            # Tampilkan pesan sukses dan kembalikan ke halaman form
            flash('Pesan Anda berhasil dikirim. Terima kasih!', 'success')
            return redirect(url_for('contact'))
            
    # Jika pengunjung hanya membuka halaman (GET)
    return render_template('contact.html')

# =============================================================
# Route Dashboard & Autentikasi (Tahap 5)
# =============================================================
# Decorator untuk membatasi akses halaman admin
# Halaman dengan @login_required hanya bisa diakses jika user sudah login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Akses ditolak. Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
@app.route('/dashboard/login', methods=['GET', 'POST'])
def login():
    # Jika sudah login, langsung alihkan ke dashboard
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Cari user di database berdasarkan username
        user = User.query.filter_by(username=username).first()
        
        # Cek apakah user ada dan password cocok (menggunakan werkzeug)
        if user and check_password_hash(user.password, password):
            # Simpan id user ke dalam session
            session['admin_id'] = user.id
            flash('Login berhasil! Selamat datang di Dashboard.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
            
    return render_template('dashboard/login.html')
@app.route('/dashboard/logout')
def logout():
    # Hapus data admin_id dari session
    session.pop('admin_id', None)
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('login'))
@app.route('/dashboard')
@login_required
def dashboard():
    # Menghitung statistik untuk ditampilkan di dashboard
    total_projects = Project.query.count()
    unread_messages = Message.query.filter_by(is_read=False).count()
    total_skills = Skill.query.count()
    
    return render_template('dashboard/index.html', 
                           total_projects=total_projects, 
                           unread_messages=unread_messages,
                           total_skills=total_skills)

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
