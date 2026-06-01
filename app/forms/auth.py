from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    # Campo para o username com validador para garantir que não seja enviado em branco
    username = StringField(
        'Usuário', 
        validators=[
            DataRequired(message="O campo usuário é obrigatório."),
            Length(min=4, max=50, message="O usuário deve ter entre 4 e 50 caracteres.")
        ]
    )
    
    # Campo para a senha que esconde os caracteres digitados na tela
    password = PasswordField(
        'Senha', 
        validators=[
            DataRequired(message="A senha é obrigatória.")
        ]
    )
    
    # Botão de envio do formulário
    submit = SubmitField('Entrar no Sistema')

    