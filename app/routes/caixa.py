from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.caixa import Caixa
from app.models.venda import Venda 
from app.models.usuario import Usuario  # <-- IMPORTANTE: Precisamos buscar o Supervisor no banco
from werkzeug.security import check_password_hash  # <-- IMPORTANTE: Para validar a senha com segurança
from decimal import Decimal, InvalidOperation
from datetime import datetime

caixa_bp = Blueprint('caixa', __name__, url_prefix='/caixa')

@caixa_bp.route('/controle', methods=['GET'])
@login_required
def controle():
    caixa_aberto = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    return render_template('caixa/controle.html', caixa_aberto=caixa_aberto)

from app.models.usuario import Usuario  # Certifique-se de importar o modelo

@caixa_bp.route('/abrir', methods=['POST'])
@login_required
def abrir():
    
    # 1. Checagem de caixa já aberto
    caixa_aberto = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    if caixa_aberto:
        flash('Você já possui um caixa aberto!', 'warning')
        return redirect(url_for('caixa.controle'))

    # 2. Captura dos dados do formulário
    sup_user = request.form.get('supervisor_username', '').strip()
    sup_pass = request.form.get('supervisor_password', '').strip()
    valor_inicial_str = request.form.get('valor_inicial', '0.00')

    # 3. VALIDAÇÃO RIGOROSA (Debug imediato)
    if not sup_user or not sup_pass:
        flash('Erro de Acesso: É obrigatório fornecer Usuário e Senha do Supervisor.', 'danger')
        return redirect(url_for('caixa.controle'))

    # 4. Busca e validação do Supervisor
    supervisor = Usuario.query.filter_by(username=sup_user).first()
    
    # Validações: existe? senha correta? é administrador?
    if not supervisor:
        flash('Autorização negada: Usuário supervisor não encontrado.', 'danger')
        return redirect(url_for('caixa.controle'))
        
    if not supervisor.verificar_senha(sup_pass):
        flash('Autorização negada: Senha do supervisor incorreta.', 'danger')
        return redirect(url_for('caixa.controle'))
        
    if not supervisor.is_admin:
        flash('Autorização negada: O usuário informado não possui privilégios de administrador.', 'danger')
        return redirect(url_for('caixa.controle'))

    # 5. Processamento do Valor
    try:
        valor_limpo = valor_inicial_str.replace('.', '').replace(',', '.')
        valor_inicial = Decimal(valor_limpo)
    except Exception:
        flash('Valor inicial inválido!', 'danger')
        return redirect(url_for('caixa.controle'))

    # 6. Persistência
    try:
        novo_caixa = Caixa(
            usuario_id=current_user.id,
            supervisor_id=supervisor.id,
            saldo_inicial=valor_inicial,
            status='Aberto',
            data_abertura=datetime.utcnow()
        )
        db.session.add(novo_caixa)
        db.session.commit()
        flash(f'Caixa aberto por: {current_user.username}. Autorizado por: {supervisor.username}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao salvar no banco de dados.', 'danger')
        
    return redirect(url_for('venda.pdv'))


@caixa_bp.route('/fechar', methods=['POST'])
@login_required
def fechar():
    dados = request.get_json() or {}
    username_admin = dados.get('username', '').strip()
    senha_admin = dados.get('password', '')
    dinheiro_declarado_str = dados.get('dinheiro_declarado', '0,00')

    # 1. Validação de Supervisor
    supervisor = Usuario.query.filter_by(username=username_admin).first()
    if not supervisor or not check_password_hash(supervisor.password_hash, senha_admin):
        return jsonify({'success': False, 'message': 'Credenciais do administrador inválidas.'}), 401
    
    if not (supervisor.role in ['admin', 'Administrador'] or getattr(supervisor, 'is_admin', False)):
        return jsonify({'success': False, 'message': 'Acesso negado: privilégios insuficientes.'}), 403

    # 2. Localiza caixa e consolida vendas
    caixa = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    if not caixa:
        return jsonify({'success': False, 'message': 'Nenhum caixa aberto encontrado.'}), 404
    
    try:
        # Consolidação de Vendas
        vendas = Venda.query.filter_by(usuario_id=current_user.id, status='Concluída').filter(Venda.data_venda >= caixa.data_abertura).all()
        
        caixa.total_vendas_dinheiro = sum(Decimal(str(v.total)) for v in vendas if v.forma_pagamento == 'Dinheiro')
        caixa.total_vendas_pix = sum(Decimal(str(v.total)) for v in vendas if v.forma_pagamento == 'PIX')
        caixa.total_vendas_cartao = sum(Decimal(str(v.total)) for v in vendas if v.forma_pagamento == 'Cartão')
        
        # 3. Usa o método profissional do modelo (lógica encapsulada)
        valor_fisico = Decimal(dinheiro_declarado_str.replace('.', '').replace(',', '.'))
        caixa.fechar(valor_fisico=valor_fisico, supervisor_id=supervisor.id)
        
        db.session.commit()
        return jsonify({'success': True, 'redirect': url_for('caixa.auditoria')})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@caixa_bp.route('/auditoria', methods=['GET'])
@login_required
def auditoria():
    # Verifica se é admin
    is_admin = current_user.role in ['ADMIN', 'admin', 'Administrador'] or getattr(current_user, 'is_admin', False)
    
    if is_admin:
        # Admin vê tudo
        historico_caixas = Caixa.query.filter_by(status='Fechado').order_by(Caixa.data_fechamento.desc()).all()
    else:
        # Operador vê apenas os caixas que ELE fechou
        historico_caixas = Caixa.query.filter_by(status='Fechado', usuario_id=current_user.id).order_by(Caixa.data_fechamento.desc()).all()
    
    return render_template('caixa/auditoria.html', historico_caixas=historico_caixas)


@caixa_bp.route('/detalhes/<int:caixa_id>')
@caixa_bp.route('/detalhes/<int:caixa_id>/<string:forma>')
@login_required
def detalhes(caixa_id, forma=None):
    caixa = Caixa.query.get_or_404(caixa_id)
    query = Venda.query.filter(
        Venda.usuario_id == caixa.usuario_id,
        Venda.data_venda >= caixa.data_abertura,
        Venda.data_venda <= (caixa.data_fechamento or datetime.utcnow())
    )
    
    # Se uma forma for enviada, filtra a query
    if forma:
        query = query.filter(Venda.forma_pagamento == forma)
        
    vendas = query.all()
    return render_template('caixa/detalhes.html', caixa=caixa, vendas=vendas, forma_filtro=forma)