from flask import Flask, render_template, request, redirect, session, url_for
import ibm_db
import re


app = Flask(__name__, template_folder='template')


# for connection
# conn= ""

app.secret_key = 'a'
print("Trying to connect...")
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=chb27028;PWD=67WHsbarLi1VaMSO;", '', '')
print("connected..")

@app.route('/')
def default():
   return render_template('Home.html')

@app.route('/home')
def home():
   return render_template('Home.html')

# Registration form

@app.route('/user-login', methods=['GET', 'POST'])
def userLogin():
    global userid
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        repass = request.form['repass']
        print("inside checking")
        print(name)
        if len(name) == 0 or len(email) == 0 or len(password) == 0 or len(repass) == 0:
            msg = "Form is not filled completely!!"
            print(msg)
            return render_template('User-login.html', msg=msg)
        elif password != repass:
            msg = "Password is not matched"
            print(msg)
            return render_template('User-login.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email'
            print(msg)
            return render_template('User-login.html', msg=msg)
        elif not re.match(r'[A-Za-z]+', name):
            msg = "Enter valid name"
            print(msg)
            return render_template('User-login.html', msg=msg)

        sql = "select * from users where name = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Acccount already exists'
        else:
            userid = name
            insert_sql = "insert into users values(?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            print("successs")
            msg = "succesfully signed up"
        return render_template('User-dashboard.html', msg=msg, name=name)
    else:
        return render_template('User-login.html')

@app.route('/agent-login', methods=['GET', 'POST'])
def adminLogin():
    global userid
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        repass = request.form['repass']
        print("inside checking")
        print(name)
        if len(name) == 0 or len(email) == 0 or len(password) == 0 or len(repass) == 0:
            msg = "Form is not filled completely!!"
            print(msg)
            return render_template('Agent-login.html', msg=msg)
        elif password != repass:
            msg = "Password is not matched"
            print(msg)
            return render_template('Agent-login.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email'
            print(msg)
            return render_template('Agent-login.html', msg=msg)
        elif not re.match(r'[A-Za-z]+', name):
            msg = "Enter valid name"
            print(msg)
            return render_template('Agent-login.html', msg=msg)

        sql = "select * from agents where name = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Acccount already exists'
        else:
            userid = name
            insert_sql = "insert into agents values(?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            print("successs")
            msg = "succesfully signed up"
        return render_template('Agent-dashboard.html', msg=msg, name=name)
    else:
        return render_template('Admin-login.html')

@app.route('/agent-login')
def agentLogin():
   return render_template('Agent-login.html')

# Login form

@app.route('/login', methods=["GET", "POST"])
def login():
    global userid
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        userid = username
        password = request.form['pass']
        if userid == 'Tharane' and password == 'Tharane':
            print("its admin")
            return render_template('Admin-dashboard.html')
        else:
            sql = "select * from agents where username = ? and password = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print(account)
            if account:
                session['Loggedin'] = True
                session['id'] = account['USERNAME']
                userid = account['USERNAME']
                session['username'] = account['USERNAME']
                msg = 'logged in successfully'

                # for getting complaints details
                sql = "select * from complaints where agent = ?"
                complaints = []
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, name)
                ibm_db.execute(stmt)
                dictionary = ibm_db.fetch_assoc(stmt)
                while dictionary != False:
                    complaints.append(dictionary)
                    dictionary = ibm_db.fetch_assoc(stmt)
                print(complaints)
                return render_template('Agent-dashboard.html', name=account['NAME'], complaints=complaints)

        sql = "select * from users where name = ? and password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account['NAME']
            userid = account['NAME']
            session['name'] = account['NAME']
            msg = 'logged in successfully'

            # for getting complaints details
            sql = "select * from complaints where name = ?"
            complaints = []
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.execute(stmt)
            dictionary = ibm_db.fetch_assoc(stmt)
            while dictionary != False:
                # print "The ID is : ",  dictionary["EMPNO"]
                # print "The Name is : ", dictionary[1]
                complaints.append(dictionary)
                dictionary = ibm_db.fetch_assoc(stmt)

            print(complaints)
            return render_template('User-dashboard.html', name=account['NAME'], complaints=complaints)
        else:
            msg = 'Incorrect user credentials'
            return render_template('User-dashboard.html', msg=msg)
    else:
        return render_template('User-login.html')

# Creating issues

@app.route('/issue', methods=["GET", "POST"])
def issue():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        text = request.form['text']
        date = request.form['date']
        try:
            sql = "insert into complaints(name,email,text,date) values(?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, email)
            ibm_db.bind_param(stmt, 3, text)
            ibm_db.bind_param(stmt, 4, date)
            ibm_db.execute(stmt)
        except:
            print(name)
            print(email)
            print(text)
            print(date)
            print("cant insert")
        sql = "select * from complaints where name = ?"
        complaints = []
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_assoc(stmt)
        while dictionary != False:
            # print "The ID is : ",  dictionary["EMPNO"]
            # print "The Name is : ", dictionary[1]
            complaints.append(dictionary)
            dictionary = ibm_db.fetch_assoc(stmt)
        print(complaints)
        return render_template('User-dashboard.html', name=name, complaints=complaints)


@app.route('/forgot')
def forgot():
   return render_template('forgot.html')

@app.route('/admin-dashboard')
def adminDashboard():
   return render_template('Admin-dashboard.html')

@app.route('/agent-dashboard')
def agentDashboard():
   return render_template('Agent-dashboard.html')

@app.route('/user-dashboard')
def userDashboard():
   return render_template('User-dashboard.html')

@app.route('/logout')
def logout():
   return render_template('Logout.html')

@app.route('/user-account')
def userAccount():
   return render_template('User-acc.html')

@app.route('/issue')
def issuse():
   return render_template('Issue-creation.html')


if __name__ == "__main__":
    app.run(debug=True)