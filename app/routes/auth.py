from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app.forms.auth import LoginForm

# Define o Blueprint de Autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver logado, redireciona direto para o painel
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard_provisorio'))
        
    form = LoginForm()
    
    # Executa a validação do Flask-WTF e a proteção CSRF ao submeter o formulário
    if form.validate_on_submit():
        # Busca o usuário no PostgreSQL usando o username digitado
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        
        # Valida se o usuário existe, se está ativo e se a senha criptografada confere
        if usuario and usuario.ativo and usuario.verificar_senha(form.password.data):
            login_user(usuario)
            flash(f'Bem-vindo ao SGC, {usuario.nome_completo}!', 'success')
            
            # Caso o usuário tenha sido interceptado tentando acessar uma rota protegida,
            # o Flask-Login lembra a URL original e a guarda no parâmetro 'next'
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.dashboard_provisorio'))
            
        # Alerta de erro genérico para dificultar engenharia reversa maliciosa
        flash('Usuário ou senha inválidos, ou conta temporariamente inativa.', 'danger')
        
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada com sucesso. Até logo!', 'info')
    return redirect(url_for('auth.login'))

# Rota temporária em texto puro para validarmos que o login funcionou perfeitamente
@auth_bp.route('/dashboard-provisorio')
@login_required
def dashboard_provisorio():
    return (
        f"<h1>Painel SGC - Login Efetuado com Sucesso!</h1>"
        f"<p>Olá, {current_user.nome_completo}. Seu nível de acesso é: <strong>{current_user.role}</strong>.</p>"
        f"<a href='{url_for('auth.logout')}'>Clique aqui para Sair (Logout)</a>"
    )