import sqlite3
import os

def inicializar_banco():
    # Garante que a pasta data exista
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect('data/xeque_mate.db')
    cursor = conn.cursor()

    # Criando a tabela com o rigor terminológico do seu projeto
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ameacas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora TEXT NOT NULL,
        tipo_ameaca TEXT NOT NULL,
        id_mitre TEXT,
        tatica_mitre TEXT,
        risco_impacto TEXT,
        status_incidente TEXT,
        plano_resposta TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Banco de dados 'xeque_mate.db' criado com sucesso na pasta data/!")

if __name__ == "__main__":
    inicializar_banco()