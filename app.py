import os
from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from models import db, User, Project, Skill, Message
from werkzeug.security import generate_password_hash

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

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
