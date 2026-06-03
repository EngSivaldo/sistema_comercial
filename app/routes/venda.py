from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.venda import Venda            
from app.models.item_venda import ItemVenda      
from app.models.caixa import Caixa
from app.models.movimentacao_estoque import MovimentacaoEstoque
from decimal import Decimal
from datetime import datetime

venda_bp = Blueprint('venda', __name__, url_prefix='/vendas')

@venda_bp.route('/pdv', methods=['GET'])
@login_required
def pdv():
    # Verifica se o operador atual tem um caixa aberto
    caixa_aberto = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    
    if not caixa_aberto:
        flash('Atenção: Você precisa abrir o caixa antes de realizar vendas!', 'warning')
        return redirect(url_for('auth.dashboard')) # Ou para a rota de caixas se já existir
        
    clientes = Cliente.query.order_by(Cliente.nome).all()
    return render_template('vendas/pdv.html', clientes=clientes, caixa=caixa_aberto)


@venda_bp.route('/api/buscar-produto', methods=['GET'])
@login_required
def buscar_produto():
    termo = request.args.get('q', '').strip()
    if not termo:
        return jsonify([])

    # Busca por código interno exato (perfeito para leitor de código de barras) ou nome parcial
    produtos = Produto.query.filter(
        (Produto.codigo_interno == termo) | 
        (Produto.nome.ilike(f'%{termo}%'))
    ).all()

    resultado = []
    for p in produtos:
        resultado.append({
            'id': p.id,
            'codigo_interno': p.codigo_interno,
            'nome': p.nome,
            'preco_venda': float(p.preco_venda),
            'quantidade_estoque': p.quantidade_estoque,
            'estoque_baixo': p.estoque_baixo
        })
    return jsonify(resultado)


@venda_bp.route('/api/finalizar', methods=['POST'])
@login_required
def finalizar_venda():
    # Garante que o caixa continua aberto
    caixa = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    if not caixa:
        return jsonify({'sucesso': False, 'mensagem': 'Seu caixa foi fechado ou não foi localizado.'}), 400

    dados = request.get_json()
    if not dados or 'itens'not in dados or not dados['itens']:
        return jsonify({'sucesso': False, 'mensagem': 'O carrinho está vazio.'}), 400

    cliente_id = dados.get('cliente_id') or None
    forma_pagamento = dados.get('forma_pagamento')
    itens_carrinho = dados['itens'] # Lista de dicionários [{'produto_id': 1, 'quantidade': 2}]

    if forma_pagamento not in ['Dinheiro', 'PIX', 'Cartão', 'Fiado']:
        return jsonify({'sucesso': False, 'mensagem': 'Forma de pagamento inválida.'}), 400

    total_venda = Decimal('0.00')
    objetos_itens_venda = []
    objetos_movimentacoes = []

    try:
        # Processa cada item do carrinho de forma segura
        for item in itens_carrinho:
            pid = int(item['produto_id'])
            qtd = int(item['quantidade'])

            if qtd <= 0:
                return jsonify({'sucesso': False, 'mensagem': 'Quantidade inválida para um dos itens.'}), 400

            # Busca o produto diretamente no banco para pegar o preço real e estoque atualizado
            prod = db.session.get(Produto, pid)
            if not prod:
                return jsonify({'sucesso': False, 'mensagem': f'Produto ID {pid} não encontrado.'}), 404

            if prod.quantidade_estoque < qtd:
                return jsonify({'sucesso': False, 'mensagem': f'Estoque insuficiente para o produto: {prod.nome}. Disponível: {prod.quantidade_estoque}'}), 400

            # Cálculos financeiros usando Decimal
            subtotal_item = prod.preco_venda * qtd
            total_venda += subtotal_item

            # Baixa o estoque do produto
            prod.quantidade_estoque -= qtd

            # Cria o registro do item da venda
            item_venda = ItemVenda(
                produto_id=prod.id,
                quantidade=qtd,
                preco_unitario=prod.preco_venda,
                subtotal=subtotal_item
            )
            objetos_itens_venda.append(item_venda)

            # Prepara a movimentação de estoque (Auditoria)
            mov = MovimentacaoEstoque(
                tipo='Saída',
                quantidade=qtd,
                descricao=f'Venda realizada no PDV',
                produto_id=prod.id,
                usuario_id=current_user.id
            )
            objetos_movimentacoes.append(mov)

        # Cria a entidade da Venda Principal
        nova_venda = Venda(
            total=total_venda,
            forma_pagamento=forma_pagamento,
            status='Concluída',
            cliente_id=cliente_id,
            usuario_id=current_user.id
        )

        # Associa os itens preparados à venda
        for item_venda in objetos_itens_venda:
            nova_venda.itens.append(item_venda)

        db.session.add(nova_venda)

        # Adiciona as movimentações de estoque
        for mov in objetos_movimentacoes:
            db.session.add(mov)

        # Atualiza o fluxo financeiro do Caixa Aberto do operador
        if forma_pagamento == 'Dinheiro':
            caixa.total_vendas_dinheiro += total_venda
        elif forma_pagamento == 'PIX':
            caixa.total_vendas_pix += total_venda
        elif forma_pagamento == 'Cartão':
            caixa.total_vendas_cartao += total_venda
        elif forma_pagamento == 'Fiado':
            caixa.total_vendas_fiado += total_venda

        # Confirma todas as operações de forma atômica no banco
        db.session.commit()

        return jsonify({
            'sucesso': True, 
            'mensagem': 'Venda finalizada com sucesso!', 
            'venda_id': nova_venda.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'sucesso': False, 'mensagem': 'Erro interno ao processar transação no banco.'}), 500


@venda_bp.route('/api/cancelar/<int:venda_id>', methods=['POST'])
@login_required
def cancelar_venda(venda_id):
    # 1. Garante que o operador possui um caixa aberto para registrar o estorno
    caixa = Caixa.query.filter_by(usuario_id=current_user.id, status='Aberto').first()
    if not caixa:
        return jsonify({'sucesso': False, 'mensagem': 'Você precisa ter um caixa aberto para realizar um estorno.'}), 400

    # 2. Busca a venda no banco de dados
    venda = db.session.get(Venda, venda_id)
    if not venda:
        return jsonify({'sucesso': False, 'mensagem': 'Venda não localizada.'}), 404

    # 3. Evita que uma venda seja cancelada duas vezes
    if venda.status == 'Cancelada':
        return jsonify({'sucesso': False, 'mensagem': 'Esta venda já se encontra cancelada.'}), 400

    try:
        # 4. Atualiza o status da venda principal
        venda.status = 'Cancelada'

        # 5. Loop de reversão dos itens
        for item in venda.itens:
            prod = db.session.get(Produto, item.produto_id)
            if prod:
                # Devolve a quantidade original ao estoque do produto
                prod.quantidade_estoque += item.quantidade
                
                # Registra a movimentação de entrada para fins de auditoria
                mov = MovimentacaoEstoque(
                    tipo='Entrada',
                    quantidade=item.quantidade,
                    descricao=f'Estorno/Cancelamento da Venda ID {venda.id}',
                    produto_id=prod.id,
                    usuario_id=current_user.id
                )
                db.session.add(mov)

        # 6. Deduz o valor total da venda do caixa operacional do operador
        if venda.forma_pagamento == 'Dinheiro':
            caixa.total_vendas_dinheiro -= venda.total
        elif venda.forma_pagamento == 'PIX':
            caixa.total_vendas_pix -= venda.total
        elif venda.forma_pagamento == 'Cartão':
            caixa.total_vendas_cartao -= venda.total
        elif venda.forma_pagamento == 'Fiado':
            caixa.total_vendas_fiado -= venda.total

        # 7. Salva a transação inteira no banco de dados de forma segura
        db.session.commit()

        return jsonify({
            'sucesso': True, 
            'mensagem': 'Venda estornada e estoque devolvido com sucesso!'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'sucesso': False, 
            'mensagem': 'Erro interno ao processar o estorno no banco de dados.'
        }), 500
