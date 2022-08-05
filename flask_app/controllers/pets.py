from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import pet


@app.route('/pet/new')
def new_pet():
    return render_template('add_pet.html')


@app.route('/pet/create', methods=['POST'])
def create_pet():
    if not pet.Pet.vlidate_pet(request.form):
        return redirect('/pet/new')
    new_pet=pet.Pet.save(request.form)
    return redirect('/dashboard')

@app.route('/pet/<int:id>')
def show_pet(id):
    if "owner_id" not in session:
        return redirect('/')
    return render_template('pet.html', pet = pet.Pet.get_one_pet(id))

@app.route('/pet/edit/<int:id>')
def edit_pet(id):
    return render_template('edit.html', pet= pet.Pet.get_one_pet(id))

@app.route('/pet/update', methods=["POST"])
def update_pet():
    if not pet.Pet.vlidate_pet(request.form):
        return redirect(f'/pet/edit/{request.form["id"]}')
    pet.Pet.update(request.form)
    return redirect(f"/pet/{request.form['id']}")


@app.route('/delete/<int:id>', methods=['POST'])
def delete_pet(id):
    pet.Pet.delete_pet(id)
    return redirect('/dashboard')
