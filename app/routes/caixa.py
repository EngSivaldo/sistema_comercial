from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.caixa import Caixa
from decimal import Decimal
from datetime import datetime

caixa_bp = Blueprint('caixa', __name__, url_prefix='/caixa')

@caixa_bp.route('/controle', methods=['GET'])
@login_required
def controle():
    caixa_aberto = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    return render_template('caixa/controle.html', caixa_aberto=caixa_aberto)

@caixa_bp.route('/abrir', methods=['POST'])
@login_required
def abrir():
    caixa_aberto = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    if caixa_aberto:
        flash('Você já possui um caixa aberto!', 'warning')
        return redirect(url_for('caixa.controle'))
    
    valor_inicial_str = request.form.get('valor_inicial', '0.00')
    try:
        valor_inicial = Decimal(valor_inicial_str.replace(',', '.'))
    except ValueError:
        flash('Valor inicial inválido!', 'danger')
        return redirect(url_for('caixa.controle'))

    # Usando os campos exatos do seu modelo: saldo_inicial
    novo_caixa = Caixa(
        usuario_id=current_user.id,
        saldo_inicial=valor_inicial,
        status='Aberto',
        data_abertura=datetime.utcnow()
    )
    
    db.session.add(novo_caixa)
    db.session.commit()
    
    flash('Caixa aberto com sucesso! Boas vendas.', 'success')
    return redirect(url_for('venda.pdv'))

@caixa_bp.route('/fechar', methods=['POST'])
@login_required
def fechar():
    caixa_aberto = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    if not caixa_aberto:
        flash('Nenhum caixa aberto localizado.', 'warning')
        return redirect(url_for('auth.dashboard'))

    # Calcula o saldo final somando o saldo inicial + todas as modalidades de venda
    caixa_aberto.saldo_final = (
        caixa_aberto.saldo_inicial +
        caixa_aberto.total_vendas_dinheiro +
        caixa_aberto.total_vendas_pix +
        caixa_aberto.total_vendas_cartao +
        caixa_aberto.total_vendas_fiado
    )
    caixa_aberto.status = 'Fechado'
    caixa_aberto.data_fechamento = datetime.utcnow()
    
    db.session.commit()
    flash('Caixa fechado e saldos consolidados com sucesso!', 'success')
    return redirect(url_for('auth.dashboard'))