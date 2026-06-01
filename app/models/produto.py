from app import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    codigo_interno = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(150), nullable=False, index=True)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(50), index=True)
    preco_custo = db.Column(db.Numeric(10, 2), nullable=False)
    preco_venda = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0, nullable=False)
    estoque_minimo = db.Column(db.Integer, default=5, nullable=False)
    imagem_url = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    movimentacoes = db.relationship('MovimentacaoEstoque', backref='produto', lazy='dynamic', cascade="all, delete-orphan")
    itens_venda = db.relationship('ItemVenda', backref='produto', lazy='dynamic')

    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= self.estoque_minimo