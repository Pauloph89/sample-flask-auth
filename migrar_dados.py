import json

DATA_FILE = "data/threats.json"

# Nossa Tabela de Conhecimento
# No seu arquivo migrar_dados.py, o dicionário deve ficar assim:
CONHECIMENTO_MITRE = {
    "Brute Force": {"id": "T1110", "tatica": "Acesso Inicial", "rec": "Bloquear IP de origem e forçar troca de senha do usuário."},
    "SQL Injection": {"id": "T1190", "tatica": "Acesso Inicial", "rec": "Isolar servidor de BD e validar filtros de entrada na aplicação."},
    "Phishing": {"id": "T1566", "tatica": "Acesso Inicial", "rec": "Revogar sessões ativas e alertar equipe para remover o e-mail."},
    "DDoS": {"id": "T1498", "tatica": "Interrupção", "rec": "Ativar proteção de borda (WAF) e filtrar tráfego anômalo."},
    "DDoS Attack": {"id": "T1498", "tatica": "Interrupção", "rec": "Ativar proteção de borda (WAF) e filtrar tráfego anômalo."},
    "Port Scan": {"id": "T1595", "tatica": "Reconhecimento", "rec": "Fechar portas desnecessárias e monitorar tentativas de conexão."},
    "Malware Inbound": {"id": "T1588", "tatica": "Obtenção de Recursos", "rec": "Isolar a máquina afetada e realizar scan completo com antivírus."},
    "XSS": {"id": "T1059", "tatica": "Execução", "rec": "Implementar sanitização de inputs e headers de CSP."},
    "XSS Attack": {"id": "T1059", "tatica": "Execução", "rec": "Implementar sanitização de inputs e headers de CSP."}
}

def migrar():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            ameacas = json.load(f)
        
        print(f"Iniciando saneamento de {len(ameacas)} registros...")
        
        for a in ameacas:
            tipo = a.get("tipo")
            if tipo in CONHECIMENTO_MITRE:
                # Injeta os dados que estavam faltando nos registros antigos
                a["mitre_id"] = CONHECIMENTO_MITRE[tipo]["id"]
                a["mitre_tatica"] = CONHECIMENTO_MITRE[tipo]["tatica"]
                a["recomendacao"] = CONHECIMENTO_MITRE[tipo]["rec"]
            else:
                a["mitre_id"] = a.get("mitre_id", "N/A")
                a["mitre_tatica"] = a.get("mitre_tatica", "N/A")
                a["recomendacao"] = a.get("recomendacao", "Análise manual requerida.")

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(ameacas, f, indent=4, ensure_ascii=False)
        
        print("Saneamento concluído com sucesso! Verifique seu Dashboard.")
        
    except Exception as e:
        print(f"Erro na migração: {e}")

if __name__ == "__main__":
    migrar()