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

def allowed_file(filename):
    """Mengecek apakah ekstensi file diizinkan"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def parse_photo_position(form):
    """Mengambil dan memvalidasi posisi foto profil (0-100%)."""
    try:
        pos_x = int(form.get('photo_pos_x', 50))
        pos_y = int(form.get('photo_pos_y', 50))
    except (TypeError, ValueError):
        return 50, 50
    return max(0, min(100, pos_x)), max(0, min(100, pos_y))


def ensure_schema():
    """Menambahkan kolom baru ke database yang sudah ada."""
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    if not inspector.has_table('user'):
        return

    columns = {column['name'] for column in inspector.get_columns('user')}
    with db.engine.begin() as conn:
        if 'photo_pos_x' not in columns:
            conn.execute(text('ALTER TABLE user ADD COLUMN photo_pos_x INTEGER DEFAULT 50'))
        if 'photo_pos_y' not in columns:
            conn.execute(text('ALTER TABLE user ADD COLUMN photo_pos_y INTEGER DEFAULT 50'))
        if 'github' not in columns:
            conn.execute(text('ALTER TABLE user ADD COLUMN github VARCHAR(200)'))
        if 'linkedin' not in columns:
            conn.execute(text('ALTER TABLE user ADD COLUMN linkedin VARCHAR(200)'))

    if inspector.has_table('project'):
        project_columns = {column['name'] for column in inspector.get_columns('project')}
        with db.engine.begin() as conn:
            if 'github_link' not in project_columns:
                conn.execute(text('ALTER TABLE project ADD COLUMN github_link VARCHAR(300)'))


with app.app_context():
    db.create_all()
    ensure_schema()


def init_database():
    with app.app_context():
        db.create_all()
        ensure_schema()
        admin = User.query.first()
        if admin is None:
            admin_baru = User(
                username='admin',
                password=generate_password_hash('admin123'),
                name='Gilang Septian',
                email='gilang@example.com',
                github='https://github.com/gilangseptian',
                linkedin='https://www.linkedin.com/in/gilang-septian/',
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
        body = request.form.get('body', '')
        
        # Validasi Input: Pastikan tidak ada spasi kosong saja
        if not name.strip() or not email.strip() or not body.strip():
            flash('Semua field wajib diisi dengan benar!', 'danger')
        else:
            # Simpan pesan ke database
            pesan_baru = Message(name=name, email=email, subject='-', body=body)
            db.session.add(pesan_baru)
            db.session.commit()
            
            # Tampilkan pesan sukses dan kembalikan ke halaman form
            flash('Pesan Anda berhasil dikirim. Terima kasih!', 'success')
            return redirect(url_for('contact'))
            
    # Jika pengunjung hanya membuka halaman (GET)
    return render_template('contact.html')

# =============================================================
# Route Dashboard & Autentikasi
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

# =============================================================
# Route CRUD Project 
# =============================================================
@app.route('/dashboard/projects')
@login_required
def manage_projects():
    # Menampilkan daftar project, diurutkan dari yang terbaru
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('dashboard/projects.html', projects=projects)
@app.route('/dashboard/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        technology = request.form.get('technology')
        link = request.form.get('link')
        github_link = request.form.get('github_link')
        
        # Validasi dasar
        if not title or not description:
            flash('Judul dan Deskripsi wajib diisi!', 'danger')
        else:
            # Handle Upload Gambar
            filename = None
            file = request.files.get('image')
            
            if file and file.filename != '':
                if allowed_file(file.filename):
                    safe_name = secure_filename(file.filename)
                    # Tambahkan UUID agar nama file unik
                    filename = f"{uuid.uuid4().hex[:8]}_{safe_name}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                else:
                    flash('Ekstensi file gambar tidak diizinkan!', 'danger')
                    return redirect(request.url)
            new_project = Project(
                title=title,
                description=description,
                technology=technology,
                link=link,
                github_link=github_link,
                image=filename
            )
            
            db.session.add(new_project)
            db.session.commit()
            flash('Project baru berhasil ditambahkan!', 'success')
            return redirect(url_for('manage_projects'))
            
    return render_template('dashboard/add_project.html')
@app.route('/dashboard/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.technology = request.form.get('technology')
        project.link = request.form.get('link')
        project.github_link = request.form.get('github_link')
        
        
        if not project.title or not project.description:
            flash('Judul dan Deskripsi wajib diisi!', 'danger')
        else:
             # Handle Update Gambar
            file = request.files.get('image')
            
            if file and file.filename != '':
                if allowed_file(file.filename):
                    safe_name = secure_filename(file.filename)
                    filename = f"{uuid.uuid4().hex[:8]}_{safe_name}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    # Hapus gambar lama jika ada
                    if project.image:
                        old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], project.image)
                        if os.path.exists(old_filepath):
                            os.remove(old_filepath)
                            
                    project.image = filename
                else:
                    flash('Ekstensi file gambar tidak diizinkan!', 'danger')
                    return redirect(request.url)
            db.session.commit()
            flash('Project berhasil diperbarui!', 'success')
            return redirect(url_for('manage_projects'))
            
    return render_template('dashboard/edit_project.html', project=project)
@app.route('/dashboard/projects/delete/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
   
    # Hapus file gambar dari server jika ada
    if project.image:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], project.image)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(project)
    db.session.commit()
    flash('Project berhasil dihapus.', 'success')
    return redirect(url_for('manage_projects'))

# =============================================================
# Route Profil & Keahlian 
# =============================================================
@app.route('/dashboard/profile', methods=['GET', 'POST'])
@login_required
def manage_profile():
    admin = User.query.first()
    skills = Skill.query.order_by(Skill.level.desc()).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        bio = request.form.get('bio')
        github = request.form.get('github')
        linkedin = request.form.get('linkedin')
        
        if not name or not email or not bio:
            flash('Semua kolom profil wajib diisi!', 'danger')
        else:
            admin.name = name
            admin.email = email
            admin.bio = bio
            admin.github = github
            admin.linkedin = linkedin
            admin.photo_pos_x, admin.photo_pos_y = parse_photo_position(request.form)

            file = request.files.get('photo')
            if file and file.filename != '':
                if allowed_file(file.filename):
                    safe_name = secure_filename(file.filename)
                    filename = f"{uuid.uuid4().hex[:8]}_{safe_name}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)

                    if admin.photo:
                        old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], admin.photo)
                        if os.path.exists(old_filepath):
                            os.remove(old_filepath)

                    admin.photo = filename
                else:
                    flash('Ekstensi file foto tidak diizinkan!', 'danger')
                    return redirect(request.url)

            db.session.commit()
            flash('Profil berhasil diperbarui!', 'success')
            return redirect(url_for('manage_profile'))
            
    # Variabel user sebenarnya sudah disuntik oleh context_processor, 
    # tapi kita pastikan data form terupdate saat page dimuat.
    return render_template('dashboard/profile.html', user=admin, skills=skills)

@app.route('/dashboard/profile/delete-photo', methods=['POST'])
@login_required
def delete_profile_photo():
    admin = User.query.first()

    if admin.photo:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], admin.photo)
        if os.path.exists(filepath):
            os.remove(filepath)
        admin.photo = None
        admin.photo_pos_x = 50
        admin.photo_pos_y = 50
        db.session.commit()
        flash('Foto profil berhasil dihapus.', 'success')
    else:
        flash('Tidak ada foto profil yang dapat dihapus.', 'warning')

    return redirect(url_for('manage_profile'))

@app.route('/dashboard/skills/add', methods=['POST'])
@login_required
def add_skill():
    name = request.form.get('name')
    
    if name:
        new_skill = Skill(name=name)
        db.session.add(new_skill)
        db.session.commit()
        flash('Skill baru berhasil ditambahkan!', 'success')
    else:
        flash('Data skill tidak valid!', 'danger')
        
    return redirect(url_for('manage_profile'))
@app.route('/dashboard/skills/delete/<int:id>', methods=['POST'])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Keahlian berhasil dihapus.', 'success')
    return redirect(url_for('manage_profile'))

# =============================================================
# Route Kotak Pesan 
# =============================================================
@app.route('/dashboard/messages')
@login_required
def manage_messages():
    # Menampilkan semua pesan, diurutkan dari yang terbaru
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('dashboard/messages.html', messages=messages)
@app.route('/dashboard/messages/read/<int:id>', methods=['POST'])
@login_required
def read_message(id):
    msg = Message.query.get_or_404(id)
    msg.is_read = True
    db.session.commit()
    flash('Pesan ditandai telah dibaca.', 'success')
    return redirect(url_for('manage_messages'))
@app.route('/dashboard/messages/delete/<int:id>', methods=['POST'])
@login_required
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Pesan berhasil dihapus dari kotak masuk.', 'success')
    return redirect(url_for('manage_messages'))

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
