from flask import flash, redirect, render_template, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import Task, User
from .forms import LoginForm, RegisterForm


@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('tasks_list'))
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('You have successfully logged in.', "success")
            session['logged_in'] = True
            session['email'] = user.email
            session['username'] = user.username
            return redirect(url_for('tasks_list'))
        else:
            flash('Username or Password Incorrect', "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('username', None)
    flash('You have successfully logged out.', "success")
    return redirect(url_for('home'))


@app.route('/home')
def tasks_list():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    content = request.form['content']
    if not content:
        flash('Please enter text for your task')
        return redirect(url_for('tasks_list'))
    task = Task(content=content)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('tasks_list'))


@app.route('/toggle', methods=['POST'])
def toggle_status():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    task_id = request.form['task_id']
    task = Task.query.get(task_id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('tasks_list'))


@app.route('/edit', methods=['POST'])
def edit_task():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    task_id = request.form['task_id']
    edit_text = request.form['edit_text']
    if not edit_text:
        flash('Please enter text for your task')
        return redirect(url_for('tasks_list'))
    task = Task.query.get(task_id)
    task.content = edit_text
    db.session.commit()
    return redirect(url_for('tasks_list'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks_list'))


@app.route('/finished')
def resolve_tasks():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    tasks = Task.query.all()
    for task in tasks:
        if not task.done:
            task.done = True
    db.session.commit()
    return redirect(url_for('tasks_list'))
