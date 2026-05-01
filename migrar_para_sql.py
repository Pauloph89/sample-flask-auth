import json
import sqlite3
import os

def migrar_dados():
    json_path = 'data/threats.json'
    db_path = 'data/xeque_mate.db'

    # Verifica se o arquivo JSON existe antes de prosseguir
    if not os.path.exists(json_path):
        print("❌ Arquivo threats.json não encontrado. Nada para migrar.")
        return

    # 1. Carrega os dados do JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        ameacas_json = json.load(f)

    # 2. Conecta ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 3. Migra cada registro mantendo a consistência técnica
    contador = 0
    for item in ameacas_json:
        cursor.execute('''
            INSERT INTO ameacas (
                data_hora, tipo_ameaca, id_mitre, tatica_mitre, 
                risco_impacto, status_incidente, plano_resposta
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('data'),
            item.get('tipo'),
            item.get('mitre_id'),
            item.get('mitre_atack'), # Usando a chave correta do seu JSON atual
            item.get('risco'),
            item.get('status'),
            item.get('recomendacao')
        ))
        contador += 1

    conn.commit()
    conn.close()
    print(f"🚀 Sucesso! {contador} registros foram migrados para o banco SQL.")

if __name__ == "__main__":
    migrar_dados()