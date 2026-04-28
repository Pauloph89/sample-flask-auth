import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuração do caminho do arquivo de dados
DATA_FILE = "data/threats.json"

@app.route("/")
def home():
    # 1. Carregamento dos dados com tratamento de erro básico
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
            ameacas = json.load(arquivo)
    except FileNotFoundError:
        ameacas = []

    # 2. Lógica de Priorização (Engenharia de Valor)
    # Definimos pesos para que o Python saiba quem deve vir primeiro
    pesos = {"Crítico": 3, "Alto": 2, "Médio": 1, "Baixo": 0}
    ameacas_ordenadas = sorted(ameacas, key=lambda x: pesos.get(x.get('risco'), 0), reverse=True)

    # 3. Camada de Análise (Cálculo de Estatísticas)
    total_critico = len([a for a in ameacas if a.get('risco') == 'Crítico'])
    total_alto = len([a for a in ameacas if a.get('risco') == 'Alto'])
    total_geral = len(ameacas)

    return render_template(
        "index.html", 
        lista_ameacas=ameacas_ordenadas, 
        criticos=total_critico,
        altos=total_alto,
        total=total_geral
    )

@app.route("/add", methods=["POST"])
def add_threat():
    # 1. Captura de dados do formulário
    tipo = request.form.get("tipo")
    risco = request.form.get("risco")
    status = request.form.get("status")
    
    # 2. Geração de metadados automáticos (Timestamp e ID)
    with open(DATA_FILE, "r", encoding="utf-8") as arquivo:
        ameacas = json.load(arquivo)

    nova_ameaca = {
        "id": len(ameacas) + 1,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": tipo,
        "risco": risco,
        "status": status
    }

    # 3. Persistência de dados
    ameacas.append(nova_ameaca)
    with open(DATA_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(ameacas, arquivo, indent=4, ensure_ascii=False)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)