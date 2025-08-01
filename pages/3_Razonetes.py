import streamlit as st
import json
import os
from collections import defaultdict

st.title("📘 Razonetes")

DATA_PATH = "data/lancamentos.json"

def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

lancamentos = carregar_lancamentos()

contas = defaultdict(lambda: {"D": [], "C": []})

for l in lancamentos:
    contas[l["debito"]]["D"].append((l["data"], l["valor"]))
    contas[l["credito"]]["C"].append((l["data"], l["valor"]))

for conta, valores in contas.items():
    st.markdown(f"### Conta: {conta}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Débito**")
        for d in valores["D"]:
            st.write(f"{d[0]} - R$ {d[1]:.2f}")
    with col2:
        st.markdown("**Crédito**")
        for c in valores["C"]:
            st.write(f"{c[0]} - R$ {c[1]:.2f}")
