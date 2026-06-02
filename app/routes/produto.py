import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models.produto import Produto
from app.forms.produto import ProdutoForm

produto_bp = Blueprint('produto', __name__, url_prefix='/produtos')

@produto_bp.route('/')
@login_required
def listar_produtos():
    produtos = Produto.query.order_by(Produto.nome).all()
    return render_template('produtos/listar.html', produtos=produtos)

@produto_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    form = ProdutoForm()
    
    if form.validate_on_submit():
        try:
            # Geração Automática do Código Interno (SKU)
            ultimo_produto = Produto.query.order_by(Produto.id.desc()).first()
            proximo_id = (ultimo_produto.id + 1) if ultimo_produto else 1
            codigo_automatico = f"PRD{proximo_id:05d}"
            
            caminho_db_imagem = None
            if form.imagem.data:
                arquivo = form.imagem.data
                nome_seguro = secure_filename(arquivo.filename)
                nome_final_arquivo = f"{codigo_automatico}_{nome_seguro}"
                
                # AJUSTE: Apontando diretamente para static/uploads/produtos da sua árvore
                diretorio_upload = os.path.join(current_app.root_path, 'static', 'uploads', 'produtos')
                os.makedirs(diretorio_upload, exist_ok=True)
                
                caminho_completo = os.path.join(diretorio_upload, nome_final_arquivo)
                arquivo.save(caminho_completo)
                
                # AJUSTE: Salvando a URL correta com a subpasta produtos para o HTML ler perfeitamente
                caminho_db_imagem = f"uploads/produtos/{nome_final_arquivo}"

            # Instanciação do modelo com os dados tratados
            novo_produto = Produto(
                codigo_interno=codigo_automatico,
                nome=form.nome.data,
                descricao=form.descricao.data,
                categoria=form.categoria.data,
                preco_custo=form.preco_custo.data,
                preco_venda=form.preco_venda.data,
                quantidade_estoque=form.quantidade_estoque.data,
                estoque_minimo=form.estoque_minimo.data,
                imagem_url=caminho_db_imagem
            )
            
            db.session.add(novo_produto)
            db.session.commit()
            
            flash(f'Produto "{novo_produto.nome}" cadastrado com sucesso! Código gerado: {codigo_automatico}', 'success')
            return redirect(url_for('produto.listar_produtos'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro interno ao processar o cadastro: {str(e)}', 'danger')
            
    return render_template('produtos/cadastrar.html', form=form)


@produto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    # Instancia o formulário já preenchido com os dados do produto do banco
    form = ProdutoForm(obj=produto)
    
    if form.validate_on_submit():
        try:
            # Atualiza os campos com os novos dados digitados
            produto.nome = form.nome.data
            produto.descricao = form.descricao.data
            produto.categoria = form.categoria.data
            produto.preco_custo = form.preco_custo.data
            produto.preco_venda = form.preco_venda.data
            produto.quantidade_estoque = form.quantidade_estoque.data
            produto.estoque_minimo = form.estoque_minimo.data
            
            # Se o usuário enviou uma nova foto, processamos o upload igual ao cadastro
            if form.imagem.data:
                arquivo = form.imagem.data
                nome_seguro = secure_filename(arquivo.filename)
                nome_final_arquivo = f"{produto.codigo_interno}_{nome_seguro}"
                
                diretorio_upload = os.path.join(current_app.root_path, 'static', 'uploads', 'produtos')
                os.makedirs(diretorio_upload, exist_ok=True)
                
                caminho_completo = os.path.join(diretorio_upload, nome_final_arquivo)
                arquivo.save(caminho_completo)
                
                produto.imagem_url = f"uploads/produtos/{nome_final_arquivo}"
            
            db.session.commit()
            flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'success')
            return redirect(url_for('produto.listar_produtos'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar o produto: {str(e)}', 'danger')
            
    return render_template('produtos/editar.html', form=form, produto=produto)


@produto_bp.route('/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    try:
        nome_produto = produto.nome
        db.session.delete(produto)
        db.session.commit()
        flash(f'Produto "{nome_produto}" removido com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao tentar excluir o produto: {str(e)}', 'danger')
        
    return redirect(url_for('produto.listar_produtos'))