import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Rota Principal (Leitura)
@app.route("/")
def home():
    with open("data/threats.json", "r", encoding="utf-8") as arquivo:
        ameacas = json.load(arquivo)
    return render_template("index.html", lista_ameacas=ameacas)

# Nova Rota: Adicionar Ameaça (Escrita)
@app.route("/add", methods=["POST"])
def add_threat():
    tipo = request.form.get("tipo")
    risco = request.form.get("risco")
    status = request.form.get("status")

    # 1. Ler o arquivo atual
    with open("data/threats.json", "r", encoding="utf-8") as arquivo:
        ameacas = json.load(arquivo)

    # 2. Criar o novo objeto (ID automático baseado no tamanho da lista)
    nova_ameaca = {
        "id": len(ameacas) + 1,
        "tipo": tipo,
        "risco": risco,
        "status": status
    }

    # 3. Adicionar e salvar de volta no arquivo
    ameacas.append(nova_ameaca)
    with open("data/threats.json", "w", encoding="utf-8") as arquivo:
        json.dump(ameacas, arquivo, indent=4, ensure_ascii=False)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)