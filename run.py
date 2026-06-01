from app import create_app, db
from app.models.usuario import Usuario
import click

app = create_app()

@app.cli.command("create-admin")
@click.option("--username", prompt="Digite o username do admin", help="Username do administrador")
@click.option("--nome", prompt="Digite o nome completo", help="Nome completo do administrador")
@click.option("--password", prompt="Digite a senha do admin", hide_input=True, confirmation_prompt=True, help="Senha do administrador")
def create_admin(username, nome, password):
    """Cria o primeiro usuario administrador adaptado ao SGC."""
    # Verifica se o username já existe no banco
    usuario_existente = Usuario.query.filter_by(username=username).first()
    
    if usuario_existente:
        click.echo("⚠️ Erro: Já existe um usuário com este username cadastrado.")
        return

    # Instancia o modelo usando os campos exatos que você definiu
    novo_admin = Usuario(
        username=username,
        nome_completo=nome,
        role='administrador',  # Define a role que ativa o seu @property is_admin
        ativo=True
    )
    
    # Utiliza o seu método em português para criptografar a senha
    novo_admin.set_senha(password)

    try:
        db.session.add(novo_admin)
        db.session.commit()
        click.echo(f"🎉 Sucesso! Usuário Administrador '{username}' criado com êxito.")
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Erro ao salvar no banco de dados: {e}")

if __name__ == "__main__":
    app.run()