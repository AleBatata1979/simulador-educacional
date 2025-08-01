import streamlit as st
import json
import os
import pandas as pd
from collections import defaultdict

st.title("📋 Balancete de Verificação")

DATA_PATH = "data/lancamentos.json"

def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

lancamentos = carregar_lancamentos()
saldos = defaultdict(lambda: {"Débito": 0, "Crédito": 0})

for l in lancamentos:
    saldos[l["debito"]]["Débito"] += l["valor"]
    saldos[l["credito"]]["Crédito"] += l["valor"]

df = pd.DataFrame([
    {"Conta": conta,
     "Débito": valores["Débito"],
     "Crédito": valores["Crédito"],
     "Saldo": valores["Débito"] - valores["Crédito"]}
    for conta, valores in saldos.items()
])

st.dataframe(df)

total_debitos = df["Débito"].sum()
total_creditos = df["Crédito"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Débitos", f"R$ {total_debitos:,.2f}")
col2.metric("Total Créditos", f"R$ {total_creditos:,.2f}")

if abs(total_debitos - total_creditos) < 0.01:
    st.success("✅ Balancete equilibrado.")
else:
    st.error("❌ Balancete não está equilibrado.")
