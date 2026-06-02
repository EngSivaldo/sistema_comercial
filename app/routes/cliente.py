from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.cliente import Cliente

# Instancia o Blueprint dos clientes com o prefixo /clientes nas URLs
cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/')
def listar_clientes():
    # Busca todos os clientes ordenados alfabeticamente por nome
    clientes = Cliente.query.order_by(Cliente.nome).all()
    return render_template('clientes/listar.html', clientes=clientes)

@cliente_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf_cnpj = request.form.get('cpf_cnpj', '').strip() or None
        telefone = request.form.get('telefone', '').strip() or None
        whatsapp = request.form.get('whatsapp', '').strip() or None
        email = request.form.get('email', '').strip() or None
        endereco = request.form.get('endereco', '').strip() or None

        # Validação de campo obrigatório
        if not nome:
            flash('O nome do cliente é obrigatório.', 'danger')
            return render_template('clientes/cadastrar.html')

        # Validações de duplicidade para campos únicos (evita crash no banco)
        if cpf_cnpj and Cliente.query.filter_by(cpf_cnpj=cpf_cnpj).first():
            flash('Este CPF/CNPJ já está cadastrado no sistema.', 'danger')
            return render_template('clientes/cadastrar.html')

        if email and Cliente.query.filter_by(email=email).first():
            flash('Este endereço de E-mail já está cadastrado no sistema.', 'danger')
            return render_template('clientes/cadastrar.html')

        try:
            # Salva o novo cliente
            novo_cliente = Cliente(
                nome=nome,
                cpf_cnpj=cpf_cnpj,
                telefone=telefone,
                whatsapp=whatsapp,
                email=email,
                endereco=endereco
            )
            db.session.add(novo_cliente)
            db.session.commit()
            
            flash(f'Cliente "{nome}" cadastrado com sucesso!', 'success')
            return redirect(url_for('cliente.listar_clientes'))
            
        except Exception as e:
            db.session.rollback()
            flash('Ocorreu um erro interno ao cadastrar o cliente. Tente novamente.', 'danger')
            return render_template('clientes/cadastrar.html')

    return render_template('clientes/cadastrar.html')

@cliente_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    # Uso moderno do SQLAlchemy para buscar por ID ou retornar 404
    cliente = db.session.get(Cliente, id)
    if not cliente:
        flash('Cliente não encontrado.', 'danger')
        return redirect(url_for('cliente.listar_clientes'))
    
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf_cnpj = request.form.get('cpf_cnpj', '').strip() or None
        telefone = request.form.get('telefone', '').strip() or None
        whatsapp = request.form.get('whatsapp', '').strip() or None
        email = request.form.get('email', '').strip() or None
        endereco = request.form.get('endereco', '').strip() or None

        if not nome:
            flash('O nome do cliente é obrigatório.', 'danger')
            return render_template('clientes/editar.html', cliente=cliente)

        # Valida duplicidades ignorando o próprio registro que está sendo editado
        if cpf_cnpj:
            existente = Cliente.query.filter(Cliente.cpf_cnpj == cpf_cnpj, Cliente.id != id).first()
            if existente:
                flash('Este CPF/CNPJ já está sendo usado por outro cliente.', 'danger')
                return render_template('clientes/editar.html', cliente=cliente)

        if email:
            existente = Cliente.query.filter(Cliente.email == email, Cliente.id != id).first()
            if existente:
                flash('Este E-mail já está sendo usado por outro cliente.', 'danger')
                return render_template('clientes/editar.html', cliente=cliente)

        try:
            # Atualiza os dados
            cliente.nome = nome
            cliente.cpf_cnpj = cpf_cnpj
            cliente.telefone = telefone
            cliente.whatsapp = whatsapp
            cliente.email = email
            cliente.endereco = endereco

            db.session.commit()
            flash(f'Cliente "{nome}" atualizado com sucesso!', 'success')
            return redirect(url_for('cliente.listar_clientes'))
            
        except Exception:
            db.session.rollback()
            flash('Ocorreu um erro ao atualizar os dados do cliente.', 'danger')
            return render_template('clientes/editar.html', cliente=cliente)

    return render_template('clientes/editar.html', cliente=cliente)

@cliente_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_cliente(id):
    cliente = db.session.get(Cliente, id)
    if not cliente:
        flash('Cliente não encontrado ou já removido.', 'danger')
        return redirect(url_for('cliente.listar_clientes'))
        
    nome_cliente = cliente.nome
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash(f'Cliente "{nome_cliente}" removido com sucesso!', 'success')
    except Exception:
        db.session.rollback()
        # Tratamento seguro caso o cliente possua vendas vinculadas
        flash('Não é possível remover este cliente pois ele já possui histórico de vendas cadastrado.', 'danger')
    
    return redirect(url_for('cliente.listar_clientes'))