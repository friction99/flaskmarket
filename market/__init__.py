from flask import Flask,render_template,flash,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
DB_NAME = 'market.db'
app = Flask(__name__) #initialising the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' #databse configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '210e840091f978df40b5405c'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
