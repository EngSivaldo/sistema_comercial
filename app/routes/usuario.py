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
        
    usuarios = Usuario.query.order_by(Usuario.nome_completo).all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

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
            flash("Erro ao salvar o usuário.", "danger")

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

        # Se o username mudou, checa se o novo já não pertence a outro usuário
        if username != usuario.username:
            existente = Usuario.query.filter_by(username=username).first()
            if existente:
                flash("Este nome de usuário já está em uso.", "danger")
                return render_template('usuarios/editar.html', usuario=usuario)

        try:
            usuario.username = username
            usuario.nome_completo = nome_completo
            usuario.role = role
            usuario.ativo = ativo

            # Altera a senha somente se o admin digitou algo no campo
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

    # Trava de segurança: impede o admin de se auto-excluir
    if id == current_user.id:
        flash("Segurança: Você não pode excluir o seu próprio usuário administrador logado!", "danger")
        return redirect(url_for('usuario.listar_usuarios'))

    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash(f"Usuário '{usuario.nome_completo}' removido do sistema.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erro ao remover o usuário. Certifique-se de que ele não possui caixas vinculados.", "danger")

    return redirect(url_for('usuario.listar_usuarios'))