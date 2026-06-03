from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.usuario import Usuario

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.route('/')
@login_required
def listar_usuarios():
    if not current_user.is_admin:
        flash("Acesso negado! Esta área é exclusiva para administradores.", "danger")
        return redirect(url_for('auth.dashboard'))
        
    # Implementação de Paginação Profissional (10 usuários por página)
    page = request.args.get('page', 1, type=int)
    pagination = Usuario.query.order_by(Usuario.nome_completo).paginate(page=page, per_page=10, error_out=False)
    usuarios = pagination.items
    
    return render_template('usuarios/listar.html', usuarios=usuarios, pagination=pagination)

@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    if not current_user.is_admin:
        flash("Acesso negado!", "danger")
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        nome_completo = request.form.get('nome_completo', '').strip()
        senha = request.form.get('senha', '')
        role = request.form.get('role', 'operador')

        if not username or not nome_completo or not senha:
            flash("Todos os campos obrigatórios devem ser preenchidos.", "warning")
            return render_template('usuarios/cadastrar.html')

        # Regra de Produção: Validação de força de senha no Backend
        if len(senha) < 6:
            flash("Segurança enfraquecida: A senha deve conter no mínimo 6 caracteres.", "warning")
            return render_template('usuarios/cadastrar.html')

        usuario_existente = Usuario.query.filter_by(username=username).first()
        if usuario_existente:
            flash("Este nome de usuário já está cadastrado no sistema.", "danger")
            return render_template('usuarios/cadastrar.html')

        try:
            novo_usuario = Usuario(username=username, nome_completo=nome_completo, role=role)
            novo_usuario.set_senha(senha)
            db.session.add(novo_usuario)
            db.session.commit()
            flash(f"Usuário '{nome_completo}' cadastrado com sucesso!", "success")
            return redirect(url_for('usuario.listar_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash("Erro interno ao salvar o usuário.", "danger")

    return render_template('usuarios/cadastrar.html')

@usuario_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if not current_user.is_admin:
        flash("Acesso negado!", "danger")
        return redirect(url_for('auth.dashboard'))

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        nome_completo = request.form.get('nome_completo', '').strip()
        senha = request.form.get('senha', '')
        role = request.form.get('role', 'operador')
        ativo = request.form.get('ativo') == 'true'

        if not username or not nome_completo:
            flash("Nome de usuário e Nome completo são obrigatórios.", "warning")
            return render_template('usuarios/editar.html', usuario=usuario)

        if username != usuario.username:
            existente = Usuario.query.filter_by(username=username).first()
            if existente:
                flash("Este nome de usuário já está em uso.", "danger")
                return render_template('usuarios/editar.html', usuario=usuario)

        # Regra de Produção: Validação de senha na alteração opcional
        if senha and len(senha) < 6:
            flash("A nova senha informada deve conter no mínimo 6 caracteres.", "warning")
            return render_template('usuarios/editar.html', usuario=usuario)

        try:
            usuario.username = username
            usuario.nome_completo = nome_completo
            usuario.role = role
            usuario.ativo = ativo

            if senha:
                usuario.set_senha(senha)

            db.session.commit()
            flash(f"Usuário '{nome_completo}' atualizado com sucesso!", "success")
            return redirect(url_for('usuario.listar_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar o usuário.", "danger")

    return render_template('usuarios/editar.html', usuario=usuario)

@usuario_bp.route('/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_usuario(id):
    if not current_user.is_admin:
        flash("Acesso negado!", "danger")
        return redirect(url_for('auth.dashboard'))

    if id == current_user.id:
        flash("Segurança: Operação abortada! Você não pode desativar a si próprio.", "danger")
        return redirect(url_for('usuario.listar_usuarios'))

    usuario = Usuario.query.get_or_404(id)
    try:
        # ARQUITETURA SÊNIOR: Substituição de exclusão física por Soft Delete (Desativação Lógica)
        usuario.ativo = False
        db.session.commit()
        flash(f"O usuário '{usuario.nome_completo}' foi desativado com sucesso. O histórico de movimentações e caixas foi preservado para auditoria.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erro interno ao tentar alterar o status do usuário.", "danger")

    return redirect(url_for('usuario.listar_usuarios'))