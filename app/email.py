from threading import Thread
from flask_mail import Message

from flask import current_app,render_template

from . import mail,app

def send_async_mail(message):
    with app.app_context():
        mail.send(message)

def welcome_email(user):
    message=Message('Bienvenido al projecto de Pablo Lupo',
                    sender=current_app.config["MAIL_USERNAME"],
                    recipients=[user.email])
    
    message.html = render_template('email/welcome.html',user=user)
    # mail.send(message)

    thread = Thread (target=send_async_mail,args=[message])
    thread.start()
    