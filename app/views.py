from flask import Blueprint
from flask import render_template,request,flash,redirect,url_for
from .forms import LoginForm,RegisterForm
from flask_login import login_user,logout_user,login_required,current_user

from .models import User

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

	return render_template('auth/login.html',title='Login',form=form)

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
	return render_template('/auth/register.html',title='Register',form=form)

@page.route('/tasks')
@login_required
def tasks():
	return render_template('task/list.html',title='Tareas')