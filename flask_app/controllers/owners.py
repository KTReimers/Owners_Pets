from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import owner, pet
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/owner/register', methods = ['POST'])
def register():
    if not owner.Owner.validate_register(request.form):
        return redirect('/')

    data={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    ownerId = owner.Owner.save(data)
    session['owner_id'] = ownerId
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'owner_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html', pets= pet.Pet.get_pets())

@app.route('/owner/login', methods=['POST'])
def login():
    if not owner.Owner.validate_login(request.form):
        return redirect('/')
    # new_owner = owner.Owner.getByEmail(request.form)
    # if not new_owner:
    #     return redirect('/')
    # if not bcrypt.check_password_hash(new_owner.password, request.form['password']):
    #     return redirect('/')
    ownerId = owner.Owner.getByEmail(request.form)
    session['owner_id'] = ownerId.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
