from app import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False, index=True)
    cpf_cnpj = db.Column(db.String(18), unique=True, index=True)
    telefone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    endereco = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento para o histórico de compras do cliente
    vendas = db.relationship('Venda', backref='cliente', lazy='dynamic')