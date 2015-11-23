from flask import Flask, render_template, json, jsonify, request,redirect,session
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.mysql import MySQL
from sys import argv
from functools import wraps
import datetime

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'this is the application secret dEvElopmEnt kEy'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '6928542m'
app.config['MYSQL_DATABASE_DB'] = 'MEMBERS_CLUB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#Standard function definitions#
def getUsers():

	#Initiate MySQL DB Connection object
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT FORENAME, SURNAME FROM USERS")
    data = cursor.fetchall()

    cursor.close()
    con.close()
    
    return data



@app.route('/')
def primary_route():
    return render_template("welcome.html")

@app.route('/access_denied')
def non_authorized_route():
    return render_template("access_denied.html")


def check_login(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)

        return non_authorized_route()
    return wrapped_function

@app.route('/login', methods=['POST'])
def login():
    target = open("logs/server_log.log", 'w')

    _email = str(request.form['form-email'])
    _password = request.form['form-password']

    #Initiate MySQL DB Connection object
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM USERS WHERE USERNAME = '{0}'".format(_email))
    data = cursor.fetchall()

    try:
        if len(data) > 0:
            if check_password_hash(str(data[0][4]), _password):
            	session['logged_in'] = True
            	session['username'] = _email
            	if data[0][5] == 'Y':
            		session['admin'] = True
            	session['vernacular_name'] = str(data[0][1]) + " " + str(data[0][2])
                return jsonify({"status": 'OK'})
            else:
                return jsonify({"status": 'WRONG'}) 
        else:
            return jsonify({"status": 'NONE'})

    except Exception as e:
        return jsonify({"status": 'ERROR'})
    
    target.close()
    cursor.close()
    con.close()

@app.route('/home')
@check_login
def home():
	target = open("logs/server_log.log", 'w')
	message=str(session['username'])
	name=str(session['vernacular_name'])
	try:
		if 'admin' in session:
			#Render admin section
			data = getUsers()
			entries = []
			target.write("GOT TO HERE")
			for x in data:
				entry = {'title': str(x[0])}
				entries.append(entry)
				target.write(str(entry))

			return render_template('home.html', message=message, name=name, entries=entries)
		else:
			return render_template('home.html', message=message, name=name)
	except Exception as e:
		target.write(str(e))
	finally:
		target.close()

@app.route('/register', methods=['POST', 'GET'])
def register():
    _forename = str(request.form['form-first-name'])
    _surname = str(request.form['form-last-name'])
    _email = str(request.form['form-email'])
    _password = str(generate_password_hash(request.form['form-password']))
    _type = str(request.form['form-select-type'])

    if _type == 'Yes':
        _type = "Y"
    else:
        _type = "N"

    con = mysql.connect()
    cursor = con.cursor()
    data=0

    try:
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = %s", (_email))
        data = cursor.fetchall()
    except Exception, e:
        target.write(str(e))

    if len(data) > 0:
        return jsonify({"status": 'EXIST'})

    else:
        sql = """INSERT INTO USERS VALUES (null, '{0}','{1}','{2}','{3}','{4}', null)""".format(_forename, _surname, _email, _password, _type)

        try:
            cursor.execute(sql)
            con.commit()
            cursor.close()
            con.close()
            return jsonify({"status": 'OK'})

        except Exception as e:
            cursor.close()
            con.close()
            return jsonify({"status": 'ERROR'})

@app.route('/logout')
def logout():
    session.clear()
    return render_template("welcome.html", message="Hope to see you soon!")

if __name__ == "__main__":
	app.run()


