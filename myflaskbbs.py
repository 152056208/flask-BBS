from flask import Flask
from apps.admin import bp as admin_bp
from apps.home import bp as home_bp
from apps.common import bp as common_bp
from exts import db,mail
import config
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(admin_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(common_bp)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)

    return app

if __name__ == '__main__':
    app=create_app()
    app.run()
