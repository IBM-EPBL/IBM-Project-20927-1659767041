from flask import Flask, render_template
app = Flask(__name__, template_folder='template')

@app.route('/')
def default():
   return render_template('Home.html')

@app.route('/home')
def home():
   return render_template('Home.html')

@app.route('/user-login')
def userLogin():
   return render_template('User-login.html')

@app.route('/admin-login')
def adminLogin():
   return render_template('Admin-login.html')

@app.route('/agent-login')
def agentLogin():
   return render_template('Agent-login.html')

@app.route('/change-password')
def changePassword():
   return render_template('Change-password.html')

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


if __name__ == '__main__':
   app.run(debug=True)