"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# Create the database and tables within the application context
with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def root():
    """Redirects to user list @ /users"""
    return redirect("/users")

@app.route('/users')
def list_users():
    """Shows list of all users in the database"""
    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user():
    """Show form for making new user"""
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/details.html", user=user)

@app.route("/user/<int:user_id>/edit", methods=["GET"])
def show_edit(user_id):
    """Show edit form for user info"""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route("/user/<int:user_id>/edit", methods=["POST"])
def user_edit(user_id):
    """Retrieves edits to a user and returns to /users"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    """Deletes user associated with ID"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")