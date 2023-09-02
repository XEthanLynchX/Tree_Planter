from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models import user

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
  return render_template('login_and_reg.html')

@app.route('/user/login')
def user_login():
  if 'user_id' in session:
    return redirect('/dashboard')
  return redirect('/')

@app.route('/register', methods = ['POST'])
def create_user():
  if not user.User.validate_User(request.form):
    return redirect('/user/login')

  pw_hash = bcrypt.generate_password_hash(request.form['password'])
  print(pw_hash)

  data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password' : pw_hash#pw_hash
    }

  id = user.User.save_user(data)
  session['user_id'] = id
  
  return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
  data = { "email" : request.form["email"] }
  user_in_db = user.User.get_email(data)

  if not user_in_db:
    flash('Email Does Not Exist, Please Try Again', "login")
    return redirect('/')

  if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
    flash('Incorrect Password, Please Try Again', "login")
    return redirect('/')

  session['user_id'] = user_in_db.id
  return redirect('/dashboard')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')