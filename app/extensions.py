from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask import request, redirect, url_for

db = SQLAlchemy()
login_manager = LoginManager()

def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.unauthorized_handler
    def unauthorized():
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {"error": "Session expired"}, 401
        return redirect(url_for('auth.login'))

    CORS(app)
