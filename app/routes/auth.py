from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db # Importamos o db para o commit da senha
from app.models.usuario import Usuario
from app.forms.auth import LoginForm

# Define o Blueprint de Autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Se já estiver logado, redireciona conforme o nível de acesso
        if current_user.is_admin:
            return redirect(url_for('auth.dashboard'))
        return redirect(url_for('venda.pdv')) # Corrigido aqui
        
    form = LoginForm()
    
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        
        if usuario and usuario.ativo and usuario.verificar_senha(form.password.data):
            login_user(usuario)
            
            # --- INTERCEPTAÇÃO DE SEGURANÇA (PEDÁGIO) ---
            if usuario.precisa_alterar_senha:
                flash('Atenção: Você precisa alterar sua senha para continuar.', 'warning')
                return redirect(url_for('auth.primeiro_acesso'))
            
           
            next_page = request.args.get('next')
            
            if next_page:
                return redirect(next_page)
            
            # Redirecionamento baseado no nível de acesso após o login bem-sucedido
            if usuario.is_admin:
                return redirect(url_for('auth.dashboard'))
            return redirect(url_for('venda.pdv')) # Corrigido aqui
            
        flash('Usuário ou senha inválidos, ou conta temporariamente inativa.', 'danger')
        
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada com sucesso. Até logo!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    # Segurança extra: se um operador burlar a URL e cair aqui com senha temporária
    if current_user.precisa_alterar_senha:
        return redirect(url_for('auth.primeiro_acesso'))
    
    # Bloqueio de perfil: Operador de caixa não acessa o painel operacional
    if not current_user.is_admin:
        flash('Acesso restrito para administradores.', 'warning')
        return redirect(url_for('venda.pdv')) # Corrigido aqui
        
    return render_template('dashboard/dashboard.html')

@auth_bp.route('/primeiro-acesso', methods=['GET', 'POST'])
@login_required
def primeiro_acesso():
    # Se o usuário já alterou a senha, bloqueia o acesso a esta tela
    if not current_user.precisa_alterar_senha:
        if current_user.is_admin:
            return redirect(url_for('auth.dashboard'))
        return redirect(url_for('venda.pdv')) # Corrigido aqui

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha', '')
        confirma_senha = request.form.get('confirma_senha', '')

        if len(nova_senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "warning")
            return render_template('auth/primeiro_acesso.html')

        if nova_senha != confirma_senha:
            flash("As senhas não coincidem.", "danger")
            return render_template('auth/primeiro_acesso.html')

        try:
            current_user.set_senha(nova_senha)
            current_user.precisa_alterar_senha = False
            db.session.commit()
            flash("Senha alterada com sucesso!", "success")
            
            # Redirecionamento inteligente após a definição da nova senha própria
            if current_user.is_admin:
                return redirect(url_for('auth.dashboard'))
            return redirect(url_for('venda.pdv')) # Corrigido aqui
            
        except Exception:
            db.session.rollback()
            flash("Erro ao salvar nova senha.", "danger")

    return render_template('auth/primeiro_acesso.html')