import streamlit as st
import json
from pathlib import Path

st.title("📘 Plano de Contas Contábil")

DATA_PATH = Path("data/plano_contas.json")

def carregar_plano():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r") as f:
            try:
                plano = json.load(f)
                if isinstance(plano, list):
                    return [c for c in plano if isinstance(c, dict) and "codigo" in c and "nome" in c and "tipo" in c]
            except json.JSONDecodeError:
                st.error("Erro ao ler plano_contas.json. Verifique o conteúdo.")
    return []

plano = carregar_plano()

if plano:
    st.subheader("Plano de Contas Atual")
    for conta in plano:
        st.write(f"{conta['codigo']} - {conta['nome']} ({conta['tipo']})")
else:
    st.warning("Nenhuma conta encontrada ou arquivo inválido.")
