from flask_sqlalchemy import SQLAlchemy

# 1. Cria o objeto db que o resto do sistema espera encontrar
db = SQLAlchemy()

# 2. Mantém as importações que você já tem (isso não causará erro novo)
from .usuario import Usuario
from .produto import Produto
from .cliente import Cliente
from .venda import Venda
from .item_venda import ItemVenda
from .caixa import Caixa
from .movimentacao_estoque import MovimentacaoEstoque