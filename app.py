import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = "data/threats.json"

# --- CAMADA DE CONHECIMENTO (Anotação Semântica e Resposta) ---
CONHECIMENTO_MITRE = {
    "Brute Force": {"id_tecnica": "T1110", "tatica": "Acesso Inicial", "recomendacao": "Bloquear IP de origem e forçar troca de senha do usuário."},
    "SQL Injection": {"id_tecnica": "T1190", "tatica": "Acesso Inicial", "recomendacao": "Isolar servidor de BD e validar filtros de entrada na aplicação."},
    "Phishing": {"id_tecnica": "T1566", "tatica": "Acesso Inicial", "recomendacao": "Revogar sessões ativas e alertar equipe para remover o e-mail."},
    "DDoS": {"id_tecnica": "T1498", "tatica": "Interrupção", "recomendacao": "Ativar proteção de borda (WAF) e filtrar tráfego anômalo."},
    "DDoS Attack": {"id_tecnica": "T1498", "tatica": "Interrupção", "recomendacao": "Ativar proteção de borda (WAF) e filtrar tráfego anômalo."},
    "Port Scan": {"id_tecnica": "T1595", "tatica": "Reconhecimento", "recomendacao": "Fechar portas desnecessárias e monitorar tentativas de conexão."},
    "Malware Inbound": {"id_tecnica": "T1588", "tatica": "Obtenção de Recursos", "recomendacao": "Isolar a máquina afetada e realizar scan completo com antivírus."},
    "XSS Attack": {"id_tecnica": "T1059", "tatica": "Execução", "recomendacao": "Implementar sanitização de inputs e headers de CSP."},
    "XSS": {"id_tecnica": "T1059", "tatica": "Execução", "recomendacao": "Implementar sanitização de inputs e headers de CSP."}

}

@app.route("/")
def home():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            ameacas = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        ameacas = []

    pesos = {"Crítico": 3, "Alto": 2, "Médio": 1, "Baixo": 0}
    ameacas_ordenadas = sorted(ameacas, key=lambda x: pesos.get(x.get('risco'), 0), reverse=True)

    # Lógica de Sugestões UX
    risco_predominante = {}
    for a in ameacas:
        tipo, risco = a.get('tipo'), a.get('risco')
        if tipo not in risco_predominante: risco_predominante[tipo] = []
        risco_predominante[tipo].append(risco)
    
    previsoes = {tipo: max(set(ls), key=ls.count) for tipo, ls in risco_predominante.items() if ls}

    return render_template(
        "index.html", 
        lista_ameacas=ameacas_ordenadas, 
        criticos=len([a for a in ameacas if a.get('risco') == 'Crítico']),
        altos=len([a for a in ameacas if a.get('risco') == 'Alto']),
        total=len(ameacas),
        sugestoes=previsoes
    )

@app.route("/add", methods=["POST"])
def add_threat():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            ameacas = json.load(arquivo)
    except:
        ameacas = []

    tipo_selecionado = request.form.get("tipo")
    
    # Busca a recomendação técnica e dados MITRE
    info_mitre = CONHECIMENTO_MITRE.get(tipo_selecionado, {
        "id_tecnica": "N/A", 
        "tatica": "N/A", 
        "recomendacao": "Análise manual avançada requerida."
    })

    nova_ameaca = {
        "id": len(ameacas) + 1,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": tipo_selecionado,
        "risco": request.form.get("risco"),
        "status": request.form.get("status"),
        "mitre_id": info_mitre["id_tecnica"],
        "mitre_tatica": info_mitre["tatica"],
        "recomendacao": info_mitre["recomendacao"]
    }

    ameacas.append(nova_ameaca)
    with open(DATA_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(ameacas, arquivo, indent=4, ensure_ascii=False)

    return redirect(url_for("home"))

@app.route("/analytics")
def analytics():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            ameacas = json.load(arquivo)
    except:
        ameacas = []

    stats_por_tipo = {}
    risco_predominante = {}

    for a in ameacas:
        tipo, risco = a.get('tipo'), a.get('risco')
        # Conta quantidade por tipo
        stats_por_tipo[tipo] = stats_por_tipo.get(tipo, 0) + 1
        
        # Agrupa riscos para calcular a previsão
        if tipo not in risco_predominante:
            risco_predominante[tipo] = []
        risco_predominante[tipo].append(risco)

    # Gera a inteligência de previsão
    previsoes = {tipo: max(set(ls), key=ls.count) for tipo, ls in risco_predominante.items() if ls}

    # Enviamos tanto os stats quanto as previsoes para o HTML
    return render_template("analytics.html", stats=stats_por_tipo, previsoes=previsoes)

if __name__ == "__main__":
    app.run(debug=True)