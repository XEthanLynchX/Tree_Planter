from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models import tree
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
  if 'user_id' not in session:
    return redirect('/user/login')
  user = User.get_id({"id":session['user_id']})
  if not user:
    return redirect('/logout')
        
  return render_template('logged_in.html', user = user, trees = tree.Tree.get_all())

@app.route('/tree/create/process', methods=['POST'])
def process_tree():
  if 'user_id' not in session:
    return redirect('/user/login')
  if not tree.Tree.validate_tree(request.form):
    return redirect('/tree/new')

  data = {
        'user_id': session['user_id'],
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date_planted': request.form['date_planted'],
    }
  tree.Tree.save_tree(data)
  return redirect('/dashboard')

@app.route('/tree/<int:id>')
def view_tree(id):
  if 'user_id' not in session:
    return redirect('/user/login')
  user = User.get_id({"id":session['user_id']})
  return render_template('view_tree.html', user = user, tree = tree.Tree.get_id({'id': id}))

@app.route('/tree/edit/<int:id>')
def edit_tree(id):
  if 'user_id' not in session:
    return redirect('/user/login')
  user = User.get_id({"id":session['user_id']})
  return render_template('edit_tree.html', user= user, tree = tree.Tree.get_id({'id': id}))

@app.route('/tree/edit/process/<int:id>', methods=['POST'])
def process_edit_tree(id):
  if 'user_id' not in session:
    return redirect('/user/login')
  if not tree.Tree.validate_tree(request.form):
    return redirect(f'/tree/edit/{id}')
  data = {
        'id': id,
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date_planted': request.form['date_planted'],
    }
  tree.Tree.update(data)
  return redirect('/dashboard')



@app.route('/tree/destroy/<int:id>')
def destroy_tree(id):
  if 'user_id' not in session:
    return redirect('/user/login')
  tree.Tree.destroy({'id':id})
  return redirect('/dashboard')

@app.route('/tree/new')
def new_tree():
  user = User.get_id({"id":session['user_id']})
  return render_template('new_tree.html', user = user)
  
@app.route('/user/account/<int:id>')
def my_trees(id):
  data = {
        "id": id
    }
  return render_template('my_tree.html',  user = User.get_one_with_trees(data) )