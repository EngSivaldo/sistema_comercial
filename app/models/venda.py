from app import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pagamento = db.Column(db.String(30), nullable=False)  # 'Dinheiro', 'PIX', 'Cartão', 'Fiado'
    status = db.Column(db.String(20), default='Concluída', nullable=False) # 'Concluída', 'Cancelada'
    
    # Chaves Estrangeiras
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # Vendedor/Operador

    # Relacionamentos
    itens = db.relationship('ItemVenda', backref='venda', lazy='subquery', cascade="all, delete-orphan")
    usuario = db.relationship('Usuario', backref='vendas')