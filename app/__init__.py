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
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.produto import produto_bp  
    app.register_blueprint(produto_bp)       

    from app.routes.cliente import cliente_bp  
    # Registre o blueprint junto com os outros existentes
    app.register_blueprint(cliente_bp)

    from app.routes.venda import venda_bp
    app.register_blueprint(venda_bp)

    # Adicione estas duas linhas logo abaixo:
    from app.routes.caixa import caixa_bp
    app.register_blueprint(caixa_bp)
     # No topo, junto com as outras importações de rotas:
    from app.routes.usuario import usuario_bp

    # Abaixo, onde os outros blueprints são registrados (geralmente dentro de create_app):
    app.register_blueprint(usuario_bp)	

    # LINHA NOVA: Importa os modelos para que o Flask-Migrate os conheça
    from app import models

    return app
