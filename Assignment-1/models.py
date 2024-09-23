from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app import app
db = SQLAlchemy(app)

class Admin(db.Model):
  __tablename__ = 'admins'
  username = db.Column(db.String(80), primary_key= True, unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  job_openings = db.relationship('JobOpening', backref='admin', lazy=True, cascade="all, delete-orphan")

  def __init__(self, username, password):
    self.username = username
    self.set_password(password)

  def set_password(self, password):
    """Create hashed password."""
    self.password = generate_password_hash(password, method='scrypt')
  
  def __repr__(self):
    return f'<Admin {self.username}>'

class JobOpening(db.Model):
  __tablename__ = 'job_openings'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), nullable=False)
  admin_username = db.Column(db.String(80), db.ForeignKey('admins.username'), nullable=False)
  applicants_list = db.relationship('Applicant', backref='job_opening', lazy=True, cascade="all, delete-orphan")

  def __init__(self, id, title, admin_username):
    self.id = id
    self.title = title
    self.admin_username = admin_username

  def __repr__(self):
    return f'<JobOpening {self.id} {self.title}>'
    

class Applicant(db.Model):
  __tablename__ = 'applicants'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  applied_jobs = db.Column(db.Integer, db.ForeignKey('job_openings.id'))
  
  def __init__(self, id, name):
    self.id = id
    self.name = name

  def __repr__(self):
    return (f'<Applicant {self.id} {self.name}>')
   

