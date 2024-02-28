from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, emp
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')
      
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)



@views.route('/add-employee', methods=['POST'])
@login_required
def add_employee():
    name = request.form.get('name')
    password = request.form.get('password')
    email = request.form.get('email')
    phone = request.form.get('phone')

    if not all([name, password, email, phone]):
        flash('Please fill out all fields!', category='error')
    else:
        new_employee = emp(name=name, password=password, email=email, phone=phone)
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added!', category='success')

    return render_template("home.html", user=current_user)


  

@views.route('/delete-employee/<int:employee_id>', methods=['POST'])
@login_required
def delete_employee(employee_id):
    employee = emp.query.get_or_404(employee_id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
    return redirect(url_for('views.home'))


@views.route('/update-employee/<int:employee_id>', methods=['POST'])
@login_required
def update_employee(employee_id):
    employee = emp.query.get_or_404(employee_id)
    if request.method == 'POST':
        db.session.commit()
    return redirect(url_for('views.home'))


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})