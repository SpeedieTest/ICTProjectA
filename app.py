from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# Initialise the database
db = SQLAlchemy(app)

# Create db model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a funtion to return string when we add someone.
    def __repr__(self):
        return '<Name %r>' % self.id

subs = []

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/admin_homepage')
def admin_homepage():
    title = "Admin Homepage"
    names = ["John", "Mary", "Sally", "Wes"]
    return render_template("admin_homepage.html", names=names, title=title)

@app.route('/subscribe')
def subscribe():
    title = "Subscribe to My Email Newsletter"
    return render_template("subscribe.html", title=title)

@app.route('/form', methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    subs.append(f"{first_name} {last_name} | {email}")
    title = "Thank You!"
    return render_template("form.html", title=title, subs=subs)


@app.route('/users', methods=['POST', 'GET'])
def users():
    title = "User List"

    if request.method == "POST":
        user_name = request.form['name']
        new_user = Users(name=user_name)
        #push to Database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')
        except:
            return "There was an error adding user"

    else:
        users = Users.query.order_by(Users.date_created)
        return render_template("friends.html",  title=title, users=users)