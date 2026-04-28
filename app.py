from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # Simulando dados que viriam de um banco ou sensor de rede
    ameacas = [
        {"id": 1, "tipo": "Brute Force", "risco": "Alto", "status": "Bloqueado"},
        {"id": 2, "tipo": "Port Scan", "risco": "Médio", "status": "Monitorando"},
        {"id": 3, "tipo": "Malware Inbound", "risco": "Crítico", "status": "Isolado"}
    ]
    return render_template("index.html", lista_ameacas=ameacas)

@app.route("/alerta/<nivel>")
def alerta(nivel):
    return f"<h3>Alerta de Segurança</h3><p>Nível detectado: <strong>{nivel}</strong></p>"

if __name__ == "__main__":
    app.run(debug=True)