from app import db
from run import app
from sqlalchemy import text

def migrar():
    with app.app_context():
        # Subtrai 3 horas (interval '3 hours') de todas as colunas de data
        # Isso converte o UTC que estava gravado para o horário de Brasília
        sql_comando = text("""
            UPDATE caixas 
            SET data_abertura = data_abertura - INTERVAL '3 hours',
                data_fechamento = data_fechamento - INTERVAL '3 hours'
            WHERE data_fechamento IS NOT NULL;
            
            UPDATE caixas 
            SET data_abertura = data_abertura - INTERVAL '3 hours'
            WHERE data_fechamento IS NULL;
        """)
        
        db.session.execute(sql_comando)
        db.session.commit()
        print("Migração concluída: Todas as datas foram ajustadas para o horário de Brasília.")

if __name__ == "__main__":
    migrar()
