import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask_wtf'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'werkzeug'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'wtforms'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'email_validator'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask_bootstrap'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyqrcode'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyotp'])


from flask import Flask, render_template, flash, session, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from cryptography.fernet import Fernet
from flask_bootstrap import Bootstrap
from io import BytesIO
import sqlite3
import pyqrcode, pyotp

# con=sqlite3.connect('user_database.db')
# cursor = con.cursor
#cursor.execute('Create table Data (Id integer primary key, email varchar,phone_number numeric(10,0),password varchar);')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
Bootstrap(app)


class RegisterForm(FlaskForm):
    firstname = StringField(label = ('First Name'), validators = [DataRequired()])
    lastname = StringField(label = ('Last Name'), validators = [DataRequired()])
    email = StringField(label = ('Email'), validators = [DataRequired(), Email()])
    phone = StringField(label = ('Phone Number'))
    password = PasswordField(label = ('Password'), validators = [DataRequired(), \
        Length(min=8, message = 'Password should be atleast 8 Characters long')])
    password_again = PasswordField(label = ('Confirm Password'),
                                   validators = [DataRequired(), EqualTo('password', message ='Passwords do not match!')])
    submit = SubmitField(label = ('Register'))



class LoginForm(FlaskForm):
    email = StringField(label = ('Email'), validators = [DataRequired(), Email()])
    password = PasswordField(label = ('Password'), validators = [DataRequired(), \
        Length(min=8, message = 'Password should be atleast 8 Characters long')])
    submit = SubmitField(label = ('Login'))



class TwoFactorForm(FlaskForm):
    token = StringField('2FA Token', validators = [DataRequired(), Length(6, 6)])
    submit = SubmitField(label = ('Verify'))



@app.route('/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with sqlite3.connect('user_database.db') as con:
            cursor = con.cursor()
            user = cursor.execute("select * from data where email = '{0}'".format(form.email.data)).fetchall()
            if not user or not verify_password(user, form.password.data):
                flash('Invalid email or password!')
                return redirect(url_for('login'))
            else:
                return redirect(url_for('twofactorcheck', secret = user[0][7]))
    return render_template('login.html', form = form)



@app.route('/register', methods = ['GET', 'POST'])
def registration():
    form = RegisterForm()   
    if form.validate_on_submit():
        with sqlite3.connect('user_database.db') as con:
            cursor = con.cursor()
            user = cursor.execute("select * from data where email = '{0}'".format(form.email.data)).fetchall()
            if user:
                flash('Email already registered!')
                return redirect(url_for('registration'))
            key = Fernet.generate_key()
            fernet = Fernet(key)
            password_entered = form.password.data
            encrypt_password = fernet.encrypt(password_entered.encode()).decode()
            otp_secret = pyotp.random_base32()
            cursor.execute("Insert into Data(first_name,last_name,email,phone_number,password,key,secret) values('{0}', '{1}','{2}',{3},'{4}','{5}','{6}')"\
                .format(form.firstname.data,form.lastname.data,form.email.data,form.phone.data,encrypt_password,key.decode(),otp_secret))
            session['email'] = form.email.data
        return redirect(url_for('two_factor_scan'))
    return render_template('registration.html', form = form)



@app.route('/loginSuccess')
def loginsuccess():
    return render_template('loginsuccess.html')



@app.route('/<secret>/twofactorcheck', methods = ['GET', 'POST'])
def twofactorcheck(secret):
    form = TwoFactorForm()
    if form.validate_on_submit():
        if not verify_token(form.token.data, secret):
            flash('Invalid Token.')
            return redirect(url_for('twofactorcheck', secret = secret))
        return redirect(url_for('loginsuccess'))
    return render_template('two_factor_check.html', form = form)



@app.route('/twofactorscan')
def two_factor_scan():
    with sqlite3.connect('user_database.db') as con:
        cursor = con.cursor()
        user = cursor.execute("select * from data where email = '{0}'".format(session['email'])).fetchall()
    if not user:
        flash('A issue occured in registering your email. Please try again.')
        con.rollback()
        return redirect(url_for('registration'))
    return render_template('two_factor_scan.html')



@app.route('/qrcode')
def qrcode():
    with sqlite3.connect('user_database.db') as con:
        cursor = con.cursor()
        user = cursor.execute("select * from data where email = '{0}'".format(session['email'])).fetchall()
    con.commit()
    url = pyqrcode.create(get_uri(user))
    stream = BytesIO()  
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {'Content-Type': 'image/svg+xml'}



def verify_password(user,password_entered):
    print(dict)
    correct_password = Fernet(user[0][6].encode()).decrypt(user[0][5].encode()).decode()
    if correct_password == password_entered:
        return True
    return False



def get_uri(user):
    return 'otpauth://totp/2FA-Project:{0}?secret={1}&issuer=2FA-Project' \
            .format(user[0][3], user[0][7]) 



def verify_token(token, secret):
    totp = pyotp.TOTP(secret)
    return token == totp.now()

    

if __name__ == "__main__":
    app.run(debug = True)