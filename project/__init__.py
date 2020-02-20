# __init__.py

from flask import Flask, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, logout_user
from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from cryptography.fernet import Fernet
# from .models import User, Credential


# ---init SQLAlchemy so we can use it later in our models---
db = SQLAlchemy()

# /---For Admin Page---/
# > Admin Page View
# ---Override AdminIndexView for access control logic---
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        if current_user.is_authenticated and current_user.is_admin == True:
            # return self.render('admin/index.html')
            return super(MyAdminIndexView,self).index()
        else:
            return redirect(url_for('main.profile'))

class ProfileView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('main.profile'))

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('main.index'))


# ---Inherit ModelView for customize access control of the admin page
class MyModelView(ModelView):
    
    encrypt_key = ''
    f = Fernet(encrypt_key)

    # Prohabit default Create and Edit: Since it will bypass hash and encryption
    # can_create = False
    # can_edit = False
    # |-> Now set to True as implemented edited save functions

    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin == True:
            return redirect(url_for('admin.index'))
        
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login'))

    # Edit the saving functions: add hash/encryption
    # |-> is_created : Will be set to True if model was created and to False if edited

    def on_model_change(self, form, User, is_created=True):
        pw = str(form.password.data)
        User.password = generate_password_hash(pw, method='sha256')

    def on_model_change(self, form, User, is_created=False):
        pw = str(form.password.data)
        User.password = generate_password_hash(pw, method='sha256')

class MyModelCView(MyModelView):
    # override MyModelView for Credential on_model_change
    def on_model_change(self, form, Credential, is_created=True):
        key = str(form.credential_key.data)
        b_key = bytes(key)
        Credential.credential_key = self.f.encrypt(b_key)

    def on_model_change(self, form, Credential, is_created=False):
        key = str(form.credential_key.data)
        b_key = bytes(key)
        Credential.credential_key = self.f.encrypt(b_key)

# /---Admin Page END---/


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'sk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    from .models import User, Credential

    # ---Initialize Login Manager--- 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo' # set optional bootswatch theme:[cerulean]
    admin = Admin(app, name='Password Manager', template_mode='bootstrap3', index_view=MyAdminIndexView())
    # add view to generate the admin/master.html
    admin.add_view(MyModelView(User, db.session, menu_icon_type='ico', menu_icon_value='static/favicon'))
    admin.add_view(MyModelCView(Credential, db.session, menu_icon_type='ico', menu_icon_value='static/favicon'))
    admin.add_view(ProfileView(name='Back', menu_icon_type='ico', menu_icon_value='static/favicon'))  
    admin.add_view(LogoutView(name='Logout', menu_icon_type='ico', menu_icon_value='static/favicon'))  


    # Initialize database when first run 
    # Manual: command.md - create db 
    @app.before_first_request
    def initialize_database():
        db.create_all()
        admin = User(email='email', name='Admin',is_admin=True, password=generate_password_hash("password", method='sha256'))
        db.session.add(admin)
        db.session.commit()

    # --- Code for HTTP Redirect if there is HTTP port ---
    @app.before_request
    def before_request():
        if not request.is_secure and app.env != "development":
            url = request.url.replace("http://", "https://", 1)
            code = 301
            return redirect(url, code=code)

    # ---Map route to the blueprint---

    # blueprint for auth route (user login)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for main route (logged in)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app


# +-------Useful Links--------+ 

# Reference For the base/ structure of this project
# https://scotch.io/tutorials/authentication-and-authorization-with-flask-login

# Reference For flask_admin
# https://flask-admin.readthedocs.io/en/latest/introduction/

# Overiding the class for redirect admin page
# https://flask-admin.readthedocs.io/en/latest/api/mod_base/
# 
# https://stackoverflow.com/questions/32705440/how-to-add-flask-login-to-flask-admin
# 
# https://www.reddit.com/r/flask/comments/5bm54z/flaskadmin_exclude_a_view_from_the_menu/