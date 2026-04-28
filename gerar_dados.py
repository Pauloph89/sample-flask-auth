import json
import random
from datetime import datetime, timedelta

tipos = ["Brute Force", "SQL Injection", "DDoS", "Phishing", "Port Scan", "XSS Attack"]
riscos = ["Baixo", "Médio", "Alto", "Crítico"]
status_opcoes = ["Bloqueado", "Monitorando", "Isolado", "Mitigado"]

def gerar_alertas(quantidade=100):
    novas_ameacas = []
    for i in range(1, quantidade + 1):
        data_aleatoria = datetime.now() - timedelta(minutes=random.randint(1, 1000))
        alerta = {
            "id": i,
            "data": data_aleatoria.strftime("%d/%m/%Y %H:%M"),
            "tipo": random.choice(tipos),
            "risco": random.choice(riscos),
            "status": random.choice(status_opcoes)
        }
        novas_ameacas.append(alerta)
    
    with open("data/threats.json", "w", encoding="utf-8") as f:
        json.dump(novas_ameacas, f, indent=4, ensure_ascii=False)
    print(f"✅ Sucesso! {quantidade} alertas gerados em data/threats.json")

if __name__ == "__main__":
    gerar_alertas(100) # Vamos começar com 100