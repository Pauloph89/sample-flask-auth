import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = "data/threats.json"

# Tabela de Tradução Técnica (Anotação Semântica)
# Mapeia o Tipo de Ameaça para metadados do MITRE ATT&CK
CONHECIMENTO_MITRE = {
    "Brute Force": {"id_tecnica": "T1110", "tatica": "Acesso Inicial"},
    "SQL Injection": {"id_tecnica": "T1190", "tatica": "Acesso Inicial"},
    "Phishing": {"id_tecnica": "T1566", "tatica": "Acesso Inicial"},
    "DDoS Attack": {"id_tecnica": "T1498", "tatica": "Interrupção de Disponibilidade"},
    "Port Scan": {"id_tecnica": "T1595", "tatica": "Reconhecimento"},
    "Malware Inbound": {"id_tecnica": "T1588", "tatica": "Obtenção de Recursos"}
}

@app.route("/")
def home():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            ameacas = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        ameacas = []

    # 1. Lógica de Pesos e Ordenação
    pesos = {"Crítico": 3, "Alto": 2, "Médio": 1, "Baixo": 0}
    ameacas_ordenadas = sorted(ameacas, key=lambda x: pesos.get(x.get('risco'), 0), reverse=True)

    # 2. Estatísticas
    total_critico = len([a for a in ameacas if a.get('risco') == 'Crítico'])
    total_alto = len([a for a in ameacas if a.get('risco') == 'Alto'])
    total_geral = len(ameacas)

    # 3. Inteligência Preditiva (Cálculo das Sugestões)
    risco_predominante = {}
    for a in ameacas:
        tipo, risco = a.get('tipo'), a.get('risco')
        if tipo not in risco_predominante:
            risco_predominante[tipo] = []
        risco_predominante[tipo].append(risco)
    
    # Gera o dicionário de sugestões: { 'Tipo': 'Risco mais comum' }
    previsoes = {tipo: max(set(ls), key=ls.count) for tipo, ls in risco_predominante.items()}

    return render_template(
        "index.html", 
        lista_ameacas=ameacas_ordenadas, 
        criticos=total_critico,
        altos=total_alto,
        total=total_geral,
        sugestoes=previsoes
    )

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
        stats_por_tipo[tipo] = stats_por_tipo.get(tipo, 0) + 1
        if tipo not in risco_predominante:
            risco_predominante[tipo] = []
        risco_predominante[tipo].append(risco)

    previsoes = {tipo: max(set(ls), key=ls.count) for tipo, ls in risco_predominante.items()}

    return render_template("analytics.html", stats=stats_por_tipo, previsoes=previsoes)

@app.route("/add", methods=["POST"])
def add_threat():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            ameacas = json.load(arquivo)
    except:
        ameacas = []

    # PEGA O TIPO QUE VOCÊ DIGITOU NO FORMULÁRIO
    tipo_selecionado = request.form.get("tipo")
    
    # CONSULTA O DICIONÁRIO MITRE (Anotação Semântica)
    info_mitre = CONHECIMENTO_MITRE.get(tipo_selecionado, {"id_tecnica": "N/A", "tatica": "N/A"})

    # MONTA A NOVA AMEAÇA COM OS METADADOS TÉCNICOS
    nova_ameaca = {
        "id": len(ameacas) + 1,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": tipo_selecionado,
        "risco": request.form.get("risco"),
        "status": request.form.get("status"),
        # Estes campos abaixo são o que o seu contrato de bolsa exige!
        "mitre_id": info_mitre["id_tecnica"],
        "mitre_tatica": info_mitre["tatica"]
    }

    ameacas.append(nova_ameaca)
    with open(DATA_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(ameacas, arquivo, indent=4, ensure_ascii=False)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)