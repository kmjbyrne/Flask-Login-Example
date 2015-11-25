#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Keith Byrne
# Aegis of: Institute of Technology Carlow
# Date Due: 27/11/2015
# Assignment Spec: Flask login from MySQL DB
# Supervisor: Paul Barry
# Successful implementation on: Python Anywhere & Linux

from flask import Flask,render_template,jsonify,url_for,request,session,flash
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask.ext.mail import Message, Mail
import MySQLdb
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is the application secret dEvElopmEnt kEy'
app.config['SECURITY_PASSWORD_SALT'] = 'this is the application secret dEvElopmEnt kEy'

#######################
### CONFIG SETTINGS ###
#######################

host = 'localhost'
password = '6928542m'
user = 'root'
db = 'MEMBERS_CLUB'

mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config["MAIL_USERNAME"] = "c00170460@gmail.com"
app.config["MAIL_PASSWORD"] = 'itcarlowpassword'
app.config["MAIL_DEFAULT_SENDER"] = 'c00170460@gmail.com'
mail.init_app(app)

ADMINS = ['c00170460@gmail.com']


##############################
#### NON ROUTE FUNCTIONS #####
##############################

def runSQLQuery(_sql, code):
    con = MySQLdb.connect(host, user, password, db)
    cursor = con.cursor()

    if code == 0: # All select queries here
        cursor.execute(_sql)
        data = cursor.fetchall()
        return data
    elif code == 1: #All insert queries here
        try:
            cursor.execute(_sql)
            con.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    cursor.close()
    con.close()

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)



def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration)
    except:
        return False
    return email


##############################
#### APPLICATION ROUTES ######
##############################

@app.route('/')
def primary_route():
    return render_template('welcome.html')



def check_login(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return non_authorized_route()
    return wrapped_function



@app.route('/access_denied')
def non_authorized_route():
    return render_template('access_denied.html')



@app.route('/login', methods=['POST'])
def login():

    _email = str(request.form['form-email'])
    _password = str(request.form['form-password'])
    _sql = "SELECT * FROM USERS WHERE USERNAME = '{0}'".format(_email)
    data = runSQLQuery(_sql, 0)

    try:
        if len(runSQLQuery(_sql, 0)) > 0:
            if str(data[0][7]) == 'N':
                return jsonify({'status': 'NON_VERIFIED'})
            elif check_password_hash(str(data[0][4]), _password):
                session['logged_in'] = True
                session['username'] = _email
                if data[0][5] == 'Y':
                    session['admin'] = True
                session['vernacular_name'] = str(data[0][1]) + ' ' + str(data[0][2])
                return jsonify({'status': 'OK'})
            else:
                return jsonify({'status': 'WRONG'})
        else:
            return jsonify({'status': 'NONE'})
    except Exception:
        return jsonify({'status': 'ERROR'})



@app.route('/home')
@check_login
def home():
    message = str(session['username'])
    name = str(session['vernacular_name'])
    try:
        if 'admin' in session:
            _sql="SELECT FORENAME, SURNAME, USERNAME FROM USERS"
            data = runSQLQuery(_sql, 0)
            entries = []
            for x in data:
                entry = {'title': str(x[0]) + " " + str(x[1]),'email': str(x[2])}
                entries.append(entry)
            return render_template('home.html',
                message=message,name=name, entries=entries)
        else:
            #standard users will not see a dictionary of users
            return render_template('home.html', message=message, name=name)
    except Exception as e:
        return render_template('error.html', message=str(e))



@app.route('/meaning')
@check_login
def meaning():
    return render_template('meaning.html')



@app.route('/register', methods=['POST'])
def register():
	
    _forename = str(request.form['form-first-name'])
    _surname = str(request.form['form-last-name'])
    _email = str(request.form['form-email'])
    _password = str(generate_password_hash(request.form['form-password']))
    _type = request.form['form-select-type']

    target = open('server.log', 'w')
    target.write('FORM ACCEPTED')

    if _type == '1':
        _type = 'Y'
    else:
        _type = 'N'

    target.write('FORM ACCEPTED')

    _sql = "SELECT * FROM USERS WHERE USERNAME = '{0}'".format(_email)
    data = runSQLQuery(_sql, 0)


    target.write(_sql)

    if len(data) > 0:
        return jsonify({'status': 'EXIST'})
    else:
    	print("Got to here")
        # Python SQL is very sensitive to column ordering. Use null for ID value
        _sql_insert = """INSERT INTO USERS VALUES (null, '{0}','{1}','{2}','{3}','{4}', now(), 'N', null)""".format(_forename,
                _surname, _email, _password, _type)

        if runSQLQuery(_sql, 1) == True:

            data = runSQLQuery(_sql_insert, 1)

            mail_token = generate_confirmation_token(_email)
            confirm_url = url_for('confirm_email', token=mail_token, _external=True)
            html = render_template('mail.html', _name = str(_forename), confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(_email, subject, html)
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': 'ERROR'})



@app.route('/confirm/<token>')
def confirm_email(token):

    try:
        email= confirm_token(token)
    except:
        return render_template('error.html', message = 'The confirmation link is invalid or has expired.')

    data = runSQLQuery("""SELECT * FROM USERS WHERE USERNAME = '{0}'""".format(email), 0)
    if data[0][7] == "Y":
        return render_template('error.html', username = str(data[0][3]),
            message='You have already successfully verified this account [' + str(data[0][8]) + ']')
    else:
        if runSQLQuery("""UPDATE USERS SET VERIFIED ='Y', DATE_VERIFIED = now() WHERE USERNAME = '{0}'""".format(email), 1):
            return render_template('welcome.html', message='Email successfully verified, please log into to continue!')



@app.route('/logout')
def logout():
    session.clear()
    return render_template('welcome.html', message='Hope to see you soon!')



@app.errorhandler(404)
@app.errorhandler(500)
@app.route('/error')
def error(e):
    if e == 404:
        return render_template('error.html', message='This is not available, sorry about that!')
    else:
        return render_template('error.html', message='Hmmmm,\
            seems the server is acting up.Please check back\
            a little later while our team get on this issue')



if __name__ == '__main__':
    app.run()


# Notes and issues
# Library  ---------------------------------
# from flask.ext.mysqldb
# Not sure why flask sql doesn't work. py version?
# ------------------------------------------


