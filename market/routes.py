from market import app
from . import render_template, redirect, url_for, flash
from .modules import Item, User
from .forms import RegisterForm, LoginForm
from . import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        try:
            db.session.commit()
            return redirect(url_for('market'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already existed! Please try a different email!', category='danger')
    if form.errors != {}:  # If there are no errors (empty dictionary) from the validations
        for err_msg in form.errors.values():
            # print(f"There was an error with creating a user: {err_msg}")
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Logged in success! Hello {attempted_user.username}!', category='success')
            return redirect(url_for('market'))
        else:
            flash('Username and password are not match! Please try again!', category='danger')
    return render_template('login.html', form=form)

# @app.route('/about/<username>')
# def about(username):
#     display_name = username.title()
#     return f'<h1>This is the about page of {display_name}</h1>'
