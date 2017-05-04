from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from random import randrange
import hashlib
app = Flask(__name__)
mysql = MySQL()

#MySQL configurations;
app.config['MYSQL_DATABASE_USER'] = 'guest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'majormatch'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def hello():
        print("Connected!")
        return render_template("login.html")


@app.route('/Authenticate', methods=['POST'])
def Authenticate():
        print('Authentication Starting')
        emailForm = request.form['Email']
        password = request.form['Password']
        splitEmail = emailForm.strip().split(' ')
        email = splitEmail[0]
        connection = mysql.connect()
        cursor = connection.cursor()
        print(email)
        cursor.callproc('Authenticate',(email,))
        dbPass = cursor.fetchone()
        hashedPass = (hashlib.sha1((password+email).encode('UTF-8'))).hexdigest()
        if hashedPass == dbPass[0]:
                print("Authentication Sucessful")
                #Alex do this VVVV
                cursor.callproc('getProfileInformation',(str(email),))
                records = cursor.fetchall()
                major_names = []
                for record in records:
                        if record[16] != None:
				major_names.append(record[16])
                major_names = ", ".join(major_names)

                return render_template('profile.html',
                                        email=email,
                                        academic_status=records[0][1],
                                        major=major_names,
                                        gpa=records[0][2],
                                        study_habit=records[0][3],
                                        alc_use=records[0][4],
                                        cig_use=records[0][5],
                                        vape_use=records[0][6],
                                        hair=records[0][7],
                                        ethnicity=records[0][8],
                                        sex=records[0][9],
                                        height=records[0][10],
                                        week_end_bed=str(records[0][11]),
                                        week_end_wake=str(records[0][12]),
                                        week_bed=str(records[0][13]),
                                        week_wake=str(records[0][14]))
        else:
                print("Authentication Failed...")
                return render_template("FailedLogin.html")
@app.route('/Logout', methods = ['POST'])
def Logout():
    return render_template("login.html")


@app.route('/GetProfile', methods=['POST'])
def GetProfile():
    print('executing query')
    cursor = mysql.connect().cursor()
    PID = randrange(1, 95)
    cursor.callproc('GetProfile', [PID])
    data = cursor.fetchall()
    print(data)
    return render_template("profile.html")

@app.route('/Registration',methods=['POST'])
def Registration():
    return render_template(preference.html)

@app.route('/SetPref', methods = ['POST'])
def SetPref():
        return render_template("preference.html")

@app.route('/SavePref', methods = ['POST'])
def SavePref():
        cursor.callproc('getProfileInformation',(str('Ldh@redred.com'),))
        records = cursor.fetchall()
        major_names = []
        for record in records:
                if record[16] != None:
                        major_names.append(record[16])
	major_names = ", ".join(major_names)
        return render_template('profile.html',
                                email=email,
                                academic_status=records[0][1],
                                major=major_names,
                                gpa=records[0][2],
                                study_habit=records[0][3],
                                alc_use=records[0][4],
                                cig_use=records[0][5],
                                vape_use=records[0][6],
                                hair=records[0][7],
                                ethnicity=records[0][8],
                                sex=records[0][9],
                                height=records[0][10],
                                week_end_bed=str(records[0][11]),
                                week_end_wake=str(records[0][12]),
                                week_bed=str(records[0][13]),
                                week_wake=str(records[0][14]))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
