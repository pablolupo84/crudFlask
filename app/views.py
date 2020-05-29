from flask import Blueprint
from flask import render_template,request,flash,redirect,url_for,abort
from .forms import LoginForm,RegisterForm,TaskForm
from flask_login import login_user,logout_user,login_required,current_user

from .models import User,Task
from .consts import *

from . import login_manager
#Blueprint-> Permite Aplicaciones Modulables Grandes
page = Blueprint('page',__name__)

@login_manager.user_loader
def load_user(id):
	return User.get_by_id(id)

@page.app_errorhandler(404)
def page_not_found(error):
	return render_template('errors/404.html'),404 #200

@page.route('/')
def index():
	return render_template('index.html',title='Index')

@page.route('/logout')
@login_required
def logout():
	logout_user()
	flash("Cerraste sesion exitosamente!")
	return redirect(url_for('.login'))

@page.route('/login',methods=["GET","POST"])
def login():
	if current_user.is_authenticated: #usuario actual
		return redirect(url_for('.tasks'))

	form=LoginForm(request.form)
	if request.method == "POST" and form.validate():
		user=User.get_by_username(form.username.data)
		if user and user.verify_password(form.password.data):
			login_user(user) #generamos una session de usuario una vez logueado exitosamente.
			flash("Usuario autenticado Exitosamente")

			# print("Nueva session creada")
			# print("Usuario : {}".format(form.username.data))
			# print("Password: {}".format(form.password.data))
		else:
			flash("Usuario o Password Invalidos","error")

	return render_template('auth/login.html',title='Login',form=form,
							active='login')

@page.route('/register',methods=["GET","POST"])
def register():
	if current_user.is_authenticated: #usuario actual
		return redirect(url_for('.tasks'))

	form = RegisterForm(request.form)

	if request.method == "POST" and form.validate():
		user=User.create_element(form.username.data,form.password.data,form.email.data)
		print("Usuario creado de forma exitosa!")
		print(user.id)
		flash("Usuario creado exitosamente!")
		login_user(user)
		return redirect(url_for('.tasks'))
	return render_template('/auth/register.html',title='Register',form=form,
							active='register')

@page.route('/tasks')
@page.route('/tasks/<int:page>')
@login_required
def tasks(page=1,per_page=2):
	pagination=current_user.tasks.paginate(page=page,per_page=per_page)
	tasks=pagination.items
	return render_template('task/list.html',title='Tareas',tasks=tasks,
							pagination=pagination,page=page,
							active='tasks')

@page.route('/tasks/new',methods=["GET","POST"])
@login_required
def new_task():
	form= TaskForm(request.form)
	if request.method == 'POST' and form.validate():
		task= Task.create_element(form.title.data,form.description.data,current_user.id)
		if task:
			flash(TASK_GENERATED)	

	return render_template('task/new.html',title='Nueva Tarea', form=form,
							active='new_task')

@page.route('/task/show/<int:task_id>')
def get_task(task_id):
	task=Task.query.get_or_404(task_id)
	return render_template('task/show.html',title='Tarea',task=task)

@page.route('/tasks/edit/<int:task_id>',methods=["GET","POST"])
@login_required
def edit_task(task_id):
	task=Task.query.get_or_404(task_id)
	
	if task.user_id != current_user.id:
		abort(404)

	form=TaskForm(request.form,obj=task)
	if request.method == 'POST' and form.validate():
		task=Task.update_element(task.id,form.title.data,form.description.data)
		if task:
			flash(TASK_UPDATED)

	return render_template('task/edit.html',title='Editar Tarea',form=form)

@page.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
	task=Task.query.get_or_404(task_id)
	
	if task.user_id != current_user.id:
		abort(404)

	if Task.delete_element(task.id):
		flash(TASK_DELETED)

	return redirect(url_for('.tasks'))
    	