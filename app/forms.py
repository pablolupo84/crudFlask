from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, HiddenField,TextAreaField
from wtforms.fields.html5 import EmailField

from .models import User

def codi_validator(form,field):
    if field.data == "codi" or field.data == "Codi":
        raise validators.ValidationError("El username Codi no es permitido.")

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo los humanos pueden completar el registro!')

class LoginForm(Form):
    username = StringField('Username',[
        validators.length(min=4,max=50,message="El Username esta fuera de Rango")
    ])
    password = PasswordField('Password',[
        validators.Required(message='El Password es requerido')
    ])

class RegisterForm(Form):
    honeypot = HiddenField("", [ length_honeypot] )

    username = StringField('Username',[
        validators.length(min=4,max=50),
        codi_validator
    ])
    email = EmailField('Correo Electronico',[
        validators.length(min=6,max=100),
        validators.Required(message='El email es requerido'),
        validators.Email(message='Ingrese un email valido.')        
    ])

    password =PasswordField('Password',[
        validators.Required(message='El password es requerido'),
        validators.EqualTo('confirm_password',message="La conrtaseña no coincide")
    ])

    confirm_password =PasswordField('Confirm Password')
    accept = BooleanField("Acepto Terminos y Condiciones",[
        validators.DataRequired()
    ])

    def validate_username(self,username):
        if User.get_by_username(username.data):
            raise validators.ValidationError("El username ya se encuentra en uso") 

    def validate_email(self,email):
        if User.get_by_email(email.data):
            raise validators.ValidationError("El email ya se encuentra en uso")

    def validate(self):
        """Sobrescribimos la funcion validate. Primero validamos las que estan utilizadas
        en el formulario y luego las que sobreescribimos"""
        if not Form.validate(self):
            return False

        if len(self.password.data)<3:
            self.password.errors.append("El password es demasiado Corto")
            return False

        return True
  
class TaskForm(Form):
    title=StringField('Titulo',[
        validators.length(min=4,max=50,message='Titulo fuera de Rango'),
        validators.DataRequired(message='El titulo es requerido.')
    ])
    description = TextAreaField('Descripcion',[
        validators.DataRequired(message='La Descripcion es requerida.')
    ],render_kw={'rows':5})

