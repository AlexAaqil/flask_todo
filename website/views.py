from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Todo

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/todos', methods=['GET', 'POST'])
@login_required
def todos():
    if request.method == 'POST':
        todo = request.form.get('todo')

        if len(todo) < 1:
            flash('Note is too short!', category='error')
        else:
            new_todo = Todo(todo=todo, user_id=current_user.id)
            db.session.add(new_todo)
            db.session.commit()
            flash('Todo has been added!', category='success')
            
    return render_template("todos.html", user=current_user)