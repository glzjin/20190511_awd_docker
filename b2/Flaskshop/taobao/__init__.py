# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///taobaotest.db?check_same_thread=False"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c576dfde280ba255'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category ="info"




from taobao import routes
