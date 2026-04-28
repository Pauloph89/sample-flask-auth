import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = "data/threats.json"

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

    nova_ameaca = {
        "id": len(ameacas) + 1,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": request.form.get("tipo"),
        "risco": request.form.get("risco"),
        "status": request.form.get("status")
    }

    ameacas.append(nova_ameaca)
    with open(DATA_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(ameacas, arquivo, indent=4, ensure_ascii=False)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)