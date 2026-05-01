import threading
import requests
import time

# Configurações do Teste
URL = "http://127.0.0.1:5000/add"
NUM_REQUISICOES = 50  # Simulação de carga moderada
THREADS = []

def enviar_requisicao(id_teste):
    dados = {
        "tipo": "SQL Injection",
        "risco": "Crítico",
        "status": "Teste de Carga Automático"
    }
    inicio = time.time()
    try:
        response = requests.post(URL, data=dados)
        fim = time.time()
        print(f"[Thread {id_teste}] Status: {response.status_code} | Tempo: {fim - inicio:.4f}s")
    except Exception as e:
        print(f"[Thread {id_teste}] Erro: {e}")

print(f"🚀 Iniciando Teste de Carga: {NUM_REQUISICOES} requisições simultâneas...")
tempo_total_inicio = time.time()

for i in range(NUM_REQUISICOES):
    t = threading.Thread(target=enviar_requisicao, args=(i,))
    THREADS.append(t)
    t.start()

for t in THREADS:
    t.join()

tempo_total_fim = time.time()
print(f"\n✅ Teste Finalizado!")
print(f"⏱️ Tempo total de processamento: {tempo_total_fim - tempo_total_inicio:.2f}s")