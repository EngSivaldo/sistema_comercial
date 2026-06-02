from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DecimalField, IntegerField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProdutoForm(FlaskForm):
    # O campo de código foi removido daqui pois será gerado de forma 100% automatizada no backend
    
    nome = StringField('Nome do Produto', validators=[
        DataRequired(message="O nome do produto é obrigatório."),
        Length(max=150, message="O nome deve ter no máximo 150 caracteres.")
    ])
    
    descricao = TextAreaField('Descrição', validators=[Optional()])
    
    # MELHORIA 2A: Campo de Categoria transformado em caixa de seleção (SelectField)
    categoria = SelectField('Categoria do Produto', choices=[
        ('', 'Selecione uma Categoria...'),
        ('Alimentos', 'Alimentos'),
        ('Bebidas', 'Bebidas'),
        ('Limpeza', 'Limpeza'),
        ('Higiene', 'Higiene'),
        ('Eletrônicos', 'Eletrônicos'),
        ('Outros', 'Outros')
    ], validators=[DataRequired(message="Por favor, selecione uma categoria válida.")])
    
    preco_custo = DecimalField('Preço de Custo (R$)', places=2, validators=[
        DataRequired(message="O preço de custo é obrigatório."),
        NumberRange(min=0.00, message="O valor não pode ser negativo.")
    ])
    
    preco_venda = DecimalField('Preço de Venda (R$)', places=2, validators=[
        DataRequired(message="O preço de venda é obrigatório."),
        NumberRange(min=0.00, message="O valor não pode ser negativo.")
    ])
    
    quantidade_estoque = IntegerField('Quantidade em Estoque', default=0, validators=[
        DataRequired(message="A quantidade de estoque é obrigatória."),
        NumberRange(min=0, message="O estoque não pode ser negativo.")
    ])
    
    estoque_minimo = IntegerField('Estoque Mínimo de Alerta', default=5, validators=[
        DataRequired(message="O estoque mínimo é obrigatório."),
        NumberRange(min=0, message="O estoque mínimo não pode ser negativo.")
    ])
    
    # MELHORIA 2B: Campo de arquivo de imagem com filtro de extensão de segurança
    imagem = FileField('Selecionar Imagem do Produto', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Apenas arquivos de imagem são permitidos (jpg, png, jpeg, webp).'),
        Optional()
    ])
    
    submit = SubmitField('Salvar Produto')