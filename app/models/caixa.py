from app import db
from datetime import datetime

class Caixa(db.Model):
    __tablename__ = 'caixas'

    id = db.Column(db.Integer, primary_key=True)
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_fechamento = db.Column(db.DateTime, nullable=True)
    saldo_inicial = db.Column(db.Numeric(10, 2), nullable=False)
    saldo_final = db.Column(db.Numeric(10, 2), nullable=True)
    status = db.Column(db.String(10), default='Aberto', nullable=False) # 'Aberto', 'Fechado'
    
    # Sangrias, suprimentos ou movimentações oriundas de vendas direto no dinheiro
    total_vendas_dinheiro = db.Column(db.Numeric(10, 2), default=0.00)
    total_vendas_pix = db.Column(db.Numeric(10, 2), default=0.00)
    total_vendas_cartao = db.Column(db.Numeric(10, 2), default=0.00)
    total_vendas_fiado = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Chaves Estrangeiras
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # Quem operou o caixa