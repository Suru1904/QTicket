from flask import Flask, redirect, render_template as render, session, url_for
from flask_sqlalchemy import SQLAlchemy, request
from sqlalchemy import true

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/TicketUS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(55), unique=True, nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(16), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)

@app.route('/feedback', methods=["POST"])
def feedback():
    email = request.form.get('email')
    message = request.form.get('message')
    entry = Feedback(email=email, message=message)
    db.session.add(entry)
    db.session.commit()
    return redirect('/')
    
@app.route("/", methods=['GET', 'POST'])
def home():
    print(session.keys())
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        condPassword= request.form.get('confPassword')
        if password == condPassword: 
            entry = Users(name=name, phone_no=phone, email=email, password=password)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('login'))
        else: 
            session["error"] = True
            return redirect('/#register')
    session.pop('error1', None)
    return render("home.html")
  
@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route("/contact")
def contact():
    return render("contact.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 
        data = Users.query.filter_by(email=username).first()
        dbPassword = data.password
        user = data.name.split()[0]
        print(f'{username = } {password = } {user = }')
        if password == dbPassword:
            session.pop('user',None)
            session["user"] = user
            return redirect('/')
        else:
            session["error1"] = True
            return redirect('/login')
    session.pop('error', None)
    return render("login.html")

@app.route("/monuments")
def monument():
    return render("monuments.html")

@app.route("/services")
def services():
    return render("services.html")

@app.route("/templesCateg")
def templesCateg():
    return render("templesCateg.html")

@app.route("/wildLifeCateg")
def wildLifeCateg():
    return render("wildLifeCateg.html")
  
if __name__ == "__main__":
  app.run("localhost", 3300, debug=True)