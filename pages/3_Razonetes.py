import streamlit as st
import json
import os

st.title("📘 Razonetes")

DATA_PATH = "data/lancamentos.json"

@st.cache_data
def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

lancamentos = carregar_lancamentos()

st.subheader("📜 Lançamentos Registrados")
for lanc in lancamentos:
    st.write(f"{lanc['data']} | Débito: {lanc['conta_debito']} | Crédito: {lanc['conta_credito']} | R$ {float(lanc['valor']):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")
st.subheader("📗 Razonetes por Conta")

contas = {}
for lanc in lancamentos:
    valor = float(lanc["valor"])
    contas.setdefault(lanc["conta_debito"], []).append(("D", valor))
    contas.setdefault(lanc["conta_credito"], []).append(("C", valor))

for conta, movimentos in contas.items():
    st.markdown(f"**{conta}**")
    debitos = [v for t, v in movimentos if t == "D"]
    creditos = [v for t, v in movimentos if t == "C"]
    saldo = sum(debitos) - sum(creditos)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Débitos")
        for d in debitos:
            st.write(f"R$ {d:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col2:
        st.write("Créditos")
        for c in creditos:
            st.write(f"R$ {c:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col3:
        st.write("Saldo Final")
        st.metric(label="", value=f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    st.markdown("---")
