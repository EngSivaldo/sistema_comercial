from app import db
from datetime import datetime

class MovimentacaoEstoque(db.Model):
    __tablename__ = 'movimentacoes_estoque'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False) # 'Entrada', 'Saída', 'Ajuste'
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    descricao = db.Column(db.String(255))
    
    # Chaves Estrangeiras
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # Responsável pelo ajuste