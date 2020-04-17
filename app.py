from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Frida123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/tuti'

#Configuracion del objeto mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'javier.solis.guardia1@gmail.com'
app.config['MAIL_PASSWORD'] = 'chimpandolfo12'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


mail = Mail(app)

class tecnicos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(15))
    apellido = db.Column(db.String(15))
    num_carnet = db.Column(db.String(10), unique = True)
    email = db.Column(db.String(50), unique = True)
    num_cel = db.Column(db.String(8), unique = True)

class administradores(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(15))
    apellido = db.Column(db.String(15))
    num_carnet = db.Column(db.String(10), unique = True)
    email = db.Column(db.String(50), unique = True)
    num_cel = db.Column(db.String(8), unique = True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return administradores.query.get(int(user_id))

class LoginForm(FlaskForm):
    email =     StringField('email',        validators=[InputRequired(), Length(min=4, max=15)])
    password =  PasswordField('password',   validators=[InputRequired(), Length(min=2, max=80)])

class RegisterForm(FlaskForm):
    nombre =    StringField('Nombre',                   validators =    [InputRequired(),                                       Length(min = 4, max = 20)])
    apellido =  StringField('Apellido',                 validators =    [InputRequired(),                                       Length(min = 4, max = 20)])
    ci =        StringField('Carnet de Identidad',      validators =    [InputRequired(),                                       Length(min = 4, max = 20)])
    email =     StringField('email',                    validators =    [InputRequired(), Email(message='Email Invalido'),      Length(max=50)])
    cel =       StringField('Numero de Celular',        validators =    [InputRequired()])
    password =  PasswordField('password',               validators =    [InputRequired(),                                       Length(min=8, max=80)])

@app.route('/')
@login_required
def index():
    return render_template('index.html', name = current_user.nombre, notificaciones = 0)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = administradores.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', mensaje = 'Email o password incorrecto')            
    else:
        return render_template('login.html')

@app.route('/RegAdmin', methods=['GET', 'POST'])
@login_required
def Registrar_Administradores():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = administradores(
                                    nombre = form.nombre.data, 
                                    apellido = form.apellido.data, 
                                    num_carnet = form.ci.data, 
                                    email = form.email.data, 
                                    num_cel = form.cel.data, 
                                    password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('registrar.html', form = form, mensaje = 'Se creo exitosamente el Administrador', name = current_user.nombre)
    else:
        return render_template('registrar.html', form = form, name = current_user.nombre)

@app.route('/VistaEmails', methods = ['GET', 'POST'])
@login_required
def VistaEmails():
    if request.method == 'GET':
        Tecnicos = tecnicos.query.all()
        return render_template('VistaEmails.html', tecnicos = Tecnicos, name = current_user.nombre)
    else:
        msg = Message(request.form['asunto'], sender = 'ccmcomteco@gmail.com', recipients = request.form.getlist('emails'))
        msg.html = request.form['mensaje']
        mail.send(msg)
        Tecnicos = tecnicos.query.all()
        return render_template('VistaEmails.html', mensaje = 'Se envio satisfactoriamente el email', name = current_user.nombre, tecnicos = Tecnicos)

@app.route('/prueba')
def prueba():
    msg = Message('Hello', sender = 'javier.solis.guardia1@gmail.com', recipients = ['javier.solis.guardia1@gmail.com'])
    msg.html = render_template('template_email.html', name = current_user.nombre)
    mail.send(msg)
    return "Message sended"

@app.route('/RegTec', methods = ['GET','POST'])
@login_required
def RegistroTecnicos():
    if request.method == 'GET':
        Todos_Tecnicos = tecnicos.query.all()
        return render_template('VistaRegistro.html', tecnicos = Todos_Tecnicos, name = current_user.nombre)
    else:
        Nombre = request.form['nombre']
        Apellido = request.form['apellido']
        Num_carnet = request.form['carnet']
        Email = request.form['email']
        Num_cel = request.form['celular']
        Todos_Tecnicos = tecnicos.query.all()
        for tech in Todos_Tecnicos:
            if tech.nombre == Nombre or tech.apellido == Apellido or tech.num_carnet == Num_carnet or tech.email == Email or tech.num_cel == Num_cel:
                return render_template('VistaRegistro.html', msg = 'No se pudo registrar, Datos ya utilizados', name = current_user.nombre)
            else:
                nuevo_Tecnico = tecnicos(
                                            nombre = request.form['nombre'],
                                            apellido = request.form['apellido'],
                                            num_carnet = request.form['carnet'],
                                            email = request.form['email'],
                                            num_cel = request.form['celular'])
                db.session.add(nuevo_Tecnico)
                db.session.commit()
                return render_template('VistaRegistro.html', mensaje = 'Se agrego satisfactoriamente el Técnico', name = current_user.nombre)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/delete/<id>')
@login_required
def delete(id):
    tecnicos.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('RegistroTecnicos'))
    

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')