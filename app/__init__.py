from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.config import Config

# Inicialização das extensões sem acoplá-las à aplicação ainda
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensões vinculando-as à instância atual do App
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Configuração do Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça o login para acessar esta página.'
    login_manager.login_message_category = 'warning'

    # Registro de Blueprints (Serão implementados nos próximos passos)
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp)


    # LINHA NOVA: Importa os modelos para que o Flask-Migrate os conheça
    from app import models

    return app