from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='operador', nullable=False)  # 'administrador' ou 'operador'
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def set_senha(self, senha):
        self.password_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.password_hash, senha)

    @property
    def is_admin(self):
        return self.role == 'administrador'

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))