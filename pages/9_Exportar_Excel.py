import streamlit as st
import pandas as pd
import json
import os
from io import BytesIO

st.title("📥 Exportação de Relatórios em Excel")

DATA_PATH = "data/lancamentos.json"
PLANO_PATH = "data/plano_contas.json"

def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def carregar_plano():
    if os.path.exists(PLANO_PATH):
        with open(PLANO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

lancamentos = carregar_lancamentos()
plano = carregar_plano()

# Razonetes
contas_mov = {}
for lanc in lancamentos:
    valor = float(lanc["valor"])
    contas_mov.setdefault(lanc["conta_debito"], []).append(("D", valor))
    contas_mov.setdefault(lanc["conta_credito"], []).append(("C", valor))

razonetes_data = []
for conta, movimentos in contas_mov.items():
    debitos = sum(v for t, v in movimentos if t == "D")
    creditos = sum(v for t, v in movimentos if t == "C")
    saldo = debitos - creditos
    razonetes_data.append({
        "Conta": conta,
        "Débitos": debitos,
        "Créditos": creditos,
        "Saldo Final": saldo
    })
df_razonetes = pd.DataFrame(razonetes_data)

# Balancete
saldos = {}
for lanc in lancamentos:
    valor = float(lanc["valor"])
    saldos[lanc["conta_debito"]] = saldos.get(lanc["conta_debito"], 0) + valor
    saldos[lanc["conta_credito"]] = saldos.get(lanc["conta_credito"], 0) - valor

balancete_data = []
for conta, valor in saldos.items():
    if valor > 0:
        debito = valor
        credito = 0
    else:
        debito = 0
        credito = -valor
    saldo_final = debito - credito
    balancete_data.append({
        "Conta": conta,
        "Débito": debito,
        "Crédito": credito,
        "Saldo Final": saldo_final
    })
df_balancete = pd.DataFrame(balancete_data)

# DRE
def obter(conta):
    return sum(v for k, v in saldos.items() if conta.lower() in k.lower())

receita_bruta = obter("Receita de Vendas")
deducoes = 0
receita_liquida = receita_bruta - deducoes
cmv = abs(obter("Custo das Mercadorias Vendidas"))
lucro_bruto = receita_liquida - cmv
desp_admin = abs(obter("Despesas Administrativas"))
salarios = abs(obter("Salários"))
aluguel = abs(obter("Aluguel"))
despesas_op = desp_admin + salarios + aluguel
resultado_operacional = lucro_bruto - despesas_op
outras_receitas = abs(obter("Outras Receitas"))
outras_despesas = abs(obter("Outras Despesas"))
resultado_antes_ir = resultado_operacional + outras_receitas - outras_despesas
ir_percentual = 0.18
ir = resultado_antes_ir * ir_percentual
lucro_liquido = resultado_antes_ir - ir

df_dre = pd.DataFrame([
    ["Receita Bruta", receita_bruta],
    ["Deduções", deducoes],
    ["Receita Líquida", receita_liquida],
    ["CMV", cmv],
    ["Lucro Bruto", lucro_bruto],
    ["Despesas Administrativas", desp_admin],
    ["Salários", salarios],
    ["Aluguel", aluguel],
    ["Despesas Operacionais", despesas_op],
    ["Resultado Operacional", resultado_operacional],
    ["Outras Receitas", outras_receitas],
    ["Outras Despesas", outras_despesas],
    ["Resultado Antes do IR", resultado_antes_ir],
    ["IR e Contribuições (18%)", ir],
    ["Lucro Líquido", lucro_liquido]
], columns=["Item", "Valor (R$)"])

# Balanço Patrimonial
def extrair_contas(plano):
    contas = {}
    for grupo, dados in plano.items():
        subcontas = dados.get("subcontas", {})
        for s1, d1 in subcontas.items():
            for s2 in d1.get("subcontas", {}).keys():
                contas[s2] = {"grupo": grupo}
    return contas

contas_info = extrair_contas(plano)
ativos, passivos, plx = {}, {}, {}
for conta, valor in saldos.items():
    info = contas_info.get(conta)
    if not info:
        continue
    grupo = info["grupo"]
    if grupo.startswith("1."):
        ativos[conta] = valor
    elif grupo.startswith("2."):
        passivos[conta] = valor
    elif grupo.startswith("3."):
        plx[conta] = valor

df_balanco = pd.DataFrame(columns=["Conta", "Valor (R$)", "Classificação"])
for conta, valor in ativos.items():
    df_balanco.loc[len(df_balanco)] = [conta, valor, "Ativo"]
for conta, valor in passivos.items():
    df_balanco.loc[len(df_balanco)] = [conta, abs(valor), "Passivo"]
for conta, valor in plx.items():
    df_balanco.loc[len(df_balanco)] = [conta, abs(valor), "Patrimônio Líquido"]

# Exportar Excel
output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df_razonetes.to_excel(writer, index=False, sheet_name="Razonetes")
    df_balancete.to_excel(writer, index=False, sheet_name="Balancete")
    df_dre.to_excel(writer, index=False, sheet_name="DRE")
    df_balanco.to_excel(writer, index=False, sheet_name="Balanco")

st.download_button("📥 Baixar Relatórios em Excel", data=output.getvalue(), file_name="relatorios_simulador.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
