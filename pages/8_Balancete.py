import streamlit as st
import json
import os

st.title("📋 Balancete de Verificação")

DATA_PATH = "data/lancamentos.json"

@st.cache_data
def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

lancamentos = carregar_lancamentos()

saldos = {}
for lanc in lancamentos:
    debito = lanc["conta_debito"]
    credito = lanc["conta_credito"]
    valor = float(lanc["valor"])

    saldos[debito] = saldos.get(debito, 0) + valor
    saldos[credito] = saldos.get(credito, 0) - valor

st.subheader("📑 Tabela do Balancete")

debito_total = 0
credito_total = 0

st.write("| Conta | Débito | Crédito | Saldo |")
st.write("|-------|--------|---------|--------|")

for conta, valor in saldos.items():
    if valor > 0:
        debito = valor
        credito = 0
    else:
        debito = 0
        credito = -valor
    saldo_final = debito - credito
    debito_total += debito
    credito_total += credito
    st.write(f"| {conta} | R$ {debito:,.2f} | R$ {credito:,.2f} | R$ {saldo_final:,.2f} |".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")
st.write(f"**Total Débito:** R$ {debito_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.write(f"**Total Crédito:** R$ {credito_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

if round(debito_total, 2) == round(credito_total, 2):
    st.success("✅ Balancete está em equilíbrio!")
else:
    st.error("❌ Balancete está desequilibrado.")
