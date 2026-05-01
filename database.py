import sqlite3

DB_PATH = 'data/xeque_mate.db'

def get_db_connection():
    # Cria uma conexão que retorna os dados como dicionários (útil para o Flask)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def listar_ameacas():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Busca todas as ameaças ordenadas pela data mais recente
    cursor.execute('SELECT * FROM ameacas ORDER BY data_hora DESC')
    ameacas = cursor.fetchall()
    conn.close()
    return ameacas

def salvar_ameaca(dados):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ameacas (
            data_hora, tipo_ameaca, id_mitre, tatica_mitre, 
            risco_impacto, status_incidente, plano_resposta
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        dados['data'], 
        dados['tipo'], 
        dados['mitre_id'], 
        dados['mitre_atack'], # Certifique-se que esta chave vem do app.py
        dados['risco'], 
        dados['status'], 
        dados['recomendacao']
    ))
    conn.commit()
    conn.close()