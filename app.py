import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, make_response
from database import listar_ameacas, salvar_ameaca

app = Flask(__name__)

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
    # 1. Recuperação de dados com conversão para dicionário (Rastreabilidade)
    ameacas_raw = listar_ameacas()
    ameacas = [dict(row) for row in ameacas_raw]

    # 2. Cálculo de Estatísticas de Frequência para o Formulário (O que estava faltando)
    stats_frequencia = {}
    for a in ameacas:
        t = a.get('tipo_ameaca')
        stats_frequencia[t] = stats_frequencia.get(t, 0) + 1

    # 3. Lógica de Ordenação Sênior (Peso de Risco)
    pesos = {"Crítico": 3, "Alto": 2, "Médio": 1, "Baixo": 0}
    ameacas_ordenadas = sorted(ameacas, key=lambda x: pesos.get(x.get('risco_impacto'), 0), reverse=True)

    # 4. Inteligência Preditiva (Sugestão de Risco Predominante)
    risco_predominante = {}
    for a in ameacas:
        tipo, risco = a.get('tipo_ameaca'), a.get('risco_impacto')
        if tipo not in risco_predominante: risco_predominante[tipo] = []
        risco_predominante[tipo].append(risco)
    
    previsoes = {tipo: max(set(ls), key=ls.count) for tipo, ls in risco_predominante.items() if ls}

    # 5. Entrega de Contexto Completo para o Template
    return render_template(
        "index.html", 
        lista_ameacas=ameacas_ordenadas, 
        criticos=len([a for a in ameacas if a.get('risco_impacto') == 'Crítico']),
        altos=len([a for a in ameacas if a.get('risco_impacto') == 'Alto']),
        total=len(ameacas),
        sugestoes=previsoes,
        stats=stats_frequencia  # Enviando os números de cada ameaça
    )

@app.route("/add", methods=["POST"])
def add_threat():
    tipo_selecionado = request.form.get("tipo")
    
    info_mitre = CONHECIMENTO_MITRE.get(tipo_selecionado, {
        "id_tecnica": "N/A", 
        "tatica": "N/A", 
        "recomendacao": "Análise manual avançada requerida."
    })

    nova_ameaca = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": tipo_selecionado,
        "risco": request.form.get("risco"),
        "status": request.form.get("status"),
        "mitre_id": info_mitre["id_tecnica"],
        "mitre_atack": info_mitre["tatica"], # Nome da chave ajustado para o banco
        "recomendacao": info_mitre["recomendacao"]
    }

    # Agora salva diretamente no SQL via database.py
    salvar_ameaca(nova_ameaca)
    return redirect(url_for("home"))

@app.route("/analytics")
def analytics():
    ameacas_raw = listar_ameacas()
    ameacas = [dict(row) for row in ameacas_raw]

    stats_por_tipo = {}
    risco_predominante = {}

    for a in ameacas:
        tipo, risco = a.get('tipo_ameaca'), a.get('risco_impacto')
        stats_por_tipo[tipo] = stats_por_tipo.get(tipo, 0) + 1
        
        if tipo not in risco_predominante:
            risco_predominante[tipo] = []
        risco_predominante[tipo].append(risco)

    previsoes = {tipo: max(set(ls), key=ls.count) for tipo, ls in risco_predominante.items() if ls}
    return render_template("analytics.html", stats=stats_por_tipo, previsoes=previsoes)

@app.route("/exportar")
def exportar_csv():
    ameacas_raw = listar_ameacas()
    ameacas = [dict(row) for row in ameacas_raw]

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow([
        'ID', 'Data_Hora', 'Tipo_Ameaca', 'ID_MITRE', 
        'Tatica_MITRE', 'Risco_Impacto', 'Status_Incidente', 'Plano_de_Resposta'
    ])

    for a in ameacas:
        writer.writerow([
            a.get('id'), a.get('data_hora'), a.get('tipo_ameaca'),
            a.get('id_mitre'), a.get('tatica_mitre'),
            a.get('risco_impacto'), a.get('status_incidente'), a.get('plano_resposta')
        ])

    output.seek(0)
    conteudo = output.getvalue().encode('latin-1', errors='replace')
    
    response = make_response(conteudo)
    response.headers["Content-Disposition"] = "attachment; filename=dataset_xeque_mate_final.csv"
    response.headers["Content-type"] = "text/csv; charset=latin-1"
    
    return response

if __name__ == "__main__":
    app.run(debug=True)