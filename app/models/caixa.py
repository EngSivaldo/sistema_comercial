from app import db
from datetime import datetime
from decimal import Decimal

from sqlalchemy.sql import func

class Caixa(db.Model):
    __tablename__ = 'caixas'

    id = db.Column(db.Integer, primary_key=True)
    
    # Agora usa o horário do sistema (já configurado como Brasília)
    data_abertura = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    data_fechamento = db.Column(db.DateTime, nullable=True)
    
    # Valores Iniciais e Finais
    saldo_inicial = db.Column(db.Numeric(12, 2), nullable=False)
    
    # STATUS: 'Aberto', 'Fechado', 'Bloqueado'
    status = db.Column(db.String(20), default='Aberto', nullable=False)
    
    # CONFERÊNCIA DE GAVETA
    valor_declarado_dinheiro = db.Column(db.Numeric(12, 2), default=0.00)
    diferenca_fechamento = db.Column(db.Numeric(12, 2), default=0.00)
    
    # RECEBÍVEIS DIGITAIS
    total_vendas_dinheiro = db.Column(db.Numeric(12, 2), default=0.00)
    total_vendas_pix = db.Column(db.Numeric(12, 2), default=0.00)
    total_vendas_cartao = db.Column(db.Numeric(12, 2), default=0.00)
    total_vendas_fiado = db.Column(db.Numeric(12, 2), default=0.00)
    
    # RELACIONAMENTOS E AUDITORIA
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    usuario = db.relationship('Usuario', foreign_keys=[usuario_id], backref='caixas_operadas')
    supervisor = db.relationship('Usuario', foreign_keys=[supervisor_id], backref='caixas_auditadas')

    @property
    def saldo_esperado_dinheiro(self):
        """Calcula o que DEVERIA ter na gaveta."""
        return Decimal(self.saldo_inicial) + Decimal(self.total_vendas_dinheiro)

    def fechar(self, valor_fisico, supervisor_id=None):
        """Método de fechamento."""
        if self.status != 'Aberto':
            raise ValueError("Este caixa já foi fechado.")
            
        self.valor_declarado_dinheiro = Decimal(valor_fisico)
        self.diferenca_fechamento = self.valor_declarado_dinheiro - self.saldo_esperado_dinheiro
        
        # Grava o momento exato do fechamento conforme o sistema
        self.data_fechamento = datetime.now()
        
        self.status = 'Fechado'
        self.supervisor_id = supervisor_id