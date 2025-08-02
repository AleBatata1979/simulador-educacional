
import streamlit as st
import json
from pathlib import Path

st.title("📘 Plano de Contas Contábil")

DATA_PATH = Path("data/plano_contas.json")

def carregar_plano():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

plano = carregar_plano()

st.subheader("Plano de Contas Atual")
for conta in plano:
    st.write(f"{conta['codigo']} - {conta['nome']} ({conta['tipo']})")
