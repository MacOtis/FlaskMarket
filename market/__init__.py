import os
import sqlalchemy
from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.app_context().push()

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Update the SQLALCHEMY_DATABASE_URI config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/market.db')  # URI = Uniform Resource Identifier
app.config['SECRET_KEY'] = 'c8ce528d9e45590e81015e40'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

# Import routes after creating the app and db
from market import routes

# Create all the necessary tables in your database according to the models you've defined
with app.app_context():
    db.create_all()

# the order of operations is now:
#
# run.py imports app from market (which is __init__.py).
# __init__.py runs, creating app and db.
# At the end of __init__.py, routes is imported.
# routes.py runs, importing app and db from __init__.py
