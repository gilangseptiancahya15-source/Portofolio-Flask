# =============================================================
# models.py - Model Database (ORM)
# =============================================================
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
 
    __tablename__ = 'user'

    # Definisi kolom-kolom tabel
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    github = db.Column(db.String(200), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(200), nullable=True)
    photo_pos_x = db.Column(db.Integer, default=50)
    photo_pos_y = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def photo_position(self):
        x = 50 if self.photo_pos_x is None else self.photo_pos_x
        y = 50 if self.photo_pos_y is None else self.photo_pos_y
        return f'{x}% {y}%'

    def __repr__(self):
        return f'<User {self.username}>'


# =============================================================
# Model 2: Project (Tabel project portfolio)
# =============================================================
class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    technology = db.Column(db.String(300), nullable=True)
    link = db.Column(db.String(300), nullable=True)
    github_link = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        """Contoh output: <Project Web Portfolio>"""
        return f'<Project {self.title}>'


# =============================================================
# Model 3: Skill (Tabel keahlian/skill)
# =============================================================
class Skill(db.Model):

    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=50)

    def __repr__(self):
        """Contoh output: <Skill Python 85%>"""
        return f'<Skill {self.name} {self.level}%>'


# =============================================================
# Model 4: Message (Tabel pesan dari pengunjung)
# =============================================================
class Message(db.Model):
   
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        """Contoh output: <Message Dari: Budi - Kerjasama>"""
        return f'<Message Dari: {self.name} - {self.subject}>'
