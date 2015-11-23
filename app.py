from flask import Flask, render_template, json, jsonify, request,redirect,session
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.mysql import MySQL
from sys import argv
import datetime

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'this is the secret development key'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '6928542m'
app.config['MYSQL_DATABASE_DB'] = 'MEMBERS_CLUB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def primary_route():
    return render_template("welcome.html")

@app.route('/login', methods=['POST'])
def login():
    target = open("logs/server_log.log", 'w')
    target.write("step in")
    _email = str(request.form['form-email'])
    target.write("step in")
    _password = request.form['form-password']
    target.write("step in")

    
    target.write(_email + " SHOULD BE")
    target.write("SELECT * FROM USERS WHERE USERNAME = '{0}'".format(_email))

    #connect to mysql
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM USERS WHERE USERNAME = '{0}'".format(_email))
    data = cursor.fetchall()



    try:
        if len(data) > 0:
            if check_password_hash(str(data[0][4]), _password):
                session['user'] = data[0][0]
                target = open("log.log", 'w')
                target.write(_email + "not written - but render y")
                return jsonify({"status": 'OK'})
            else:
                target.write(_email + "not written - connected ok")
                return jsonify({"status": 'WRONG'}) 
        else:
            target.write(_email + "not written - EMPTY SET")
            return jsonify({"status": 'NONE'})

        #cursor.close()
        #con.close()
    except Exception as e:
        target.write(_email + "not written - EXCEPTION")
        return jsonify({"status": 'Invalid'})
    
    target.close()
    cursor.close()
    con.close()

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():

    target = open("logs/server_log.log", 'w')
    target.write("ACCESSED")

    _forename = str(request.form['form-first-name'])
    _surname = str(request.form['form-last-name'])
    _email = str(request.form['form-email'])
    _password = str(generate_password_hash(request.form['form-password']))
    _type = str(request.form['form-select-type'])

    target.write("ACCESSED4")


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
        target.write("Username exists")
        return jsonify({"status": 'EXIST'})

    else:
        sql = """INSERT INTO USERS VALUES (null, '{0}','{1}','{2}','{3}','{4}',null)""".format(_forename, _surname, _email, _password, _type)

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

if __name__ == "__main__":
	app.run()
