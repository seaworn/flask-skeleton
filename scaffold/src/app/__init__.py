import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# instantiate extensions
login_manager = LoginManager()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app():

    from config import config
    from app.user.views import user_blueprint
    from app.main.views import main_blueprint
    from app.models import User, AnonymousUser

    # instantiate app
    app = Flask(__name__)

    # set app config
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[env])
    config[env].configure(app)

    # set up extensions
    for ext in (login_manager, bootstrap, db, migrate):
        ext.init_app(app)

    # register blueprints
    for blueprint in (user_blueprint, main_blueprint):
        app.register_blueprint(blueprint)

    # set up flask login
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'info'
    login_manager.anonymous_user = AnonymousUser

    # error handlers
    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('errors/401.html', error=error), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html', error=error), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html', error=error), 500

    return app
