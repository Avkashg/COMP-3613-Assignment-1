import click, sys

import flask_sqlalchemy
from models import db, Admin, Applicant, JobOpening
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = Admin('Bob', 'bobspassword')
  job = JobOpening(id = 1,title='Python Developer', admin_username='bob')
  bob.job_openings.append(job)
  tom = Applicant('1', 'Tom')
  db.session.add(tom)
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print(job)
  print(tom)
  print('database intialized')

@app.cli.command("list-admin", help="Lists all admins")
def list_admin():
  admin = Admin.query.all()
  print(admin)

@app.cli.command('list-jobs', help = "Lists all jobs")
def get_job_listings():
  jobs = JobOpening.query.all()
  print(jobs)

@app.cli.command('create-job', help = "Creates a new job")
@click.argument('id', default = 1)
@click.argument('title', default = "Pyhton Developer")
@click.argument('admin_username', default = "bob")
def create_job(id, title, admin_username):
  bob = Admin.query.filter_by(username=admin_username).first()
  ref = JobOpening.query.filter_by(id=id).first()
  if not bob:
    print(f'User {admin_username} not found')
    return
  if ref:
    print(f'Job {id} already exists')
    return
  job = JobOpening(id=id, title=title, admin_username=admin_username)
  db.session.add(job)
  db.session.commit()
  print("Job Added!")

@app.cli.command('create-applicant', help = "Creates a new applicant")
@click.argument('id', default = 1)
@click.argument('name', default = "Tom")
def create_applicant(id, name):
  tom = Applicant.query.filter_by(id=id).first()
  if tom:
    print(f'Applicant {id} already exists')
    return
  applicant = Applicant(id=id, name=name)
  db.session.add(applicant)
  db.session.commit()
  print(f'Applicant {name} added')

@app.cli.command('apply-job', help = "Applies for a job")
@click.argument('id', default = 1)
@click.argument('name', default = "Tom")
def apply_job(id, name):
  tom = Applicant.query.filter_by(name=name).first()
  ref = JobOpening.query.filter_by(id=id).first()
  if not tom:
    print(f'User {name} not found')
    return
  if not ref:
    print(f'Job {id} not found')
    return
 
  ref.applicants_list.append(tom)
  db.session.add(ref)
  db.session.commit()
  print(f'User {name} applied to {id}')
  

@app.cli.command('list-applicants', help = "Lists all applicants applied for a specific job")
@click.argument('id', default = 1)
def get_job_applicants(id):
  ref = JobOpening.query.filter_by(id=id).first()
  if not ref:
    print(f'Job {id} not found')
    return
  print(ref.applicants_list)