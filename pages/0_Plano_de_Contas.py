import streamlit as st
import json
from pathlib import Path

st.title("📘 Plano de Contas Contábil")

DATA_PATH = Path("data/plano_contas.json")

def carregar_plano():
    if DATA_PATH.exists():
        try:
            with open(DATA_PATH, "r") as f:
                dados = json.load(f)
            if isinstance(dados, list):
                return [c for c in dados if isinstance(c, dict) and all(k in c for k in ("codigo", "nome", "tipo"))]
        except Exception as e:
            st.error(f"Erro ao carregar o plano de contas: {e}")
    return []

plano = carregar_plano()

if plano:
    st.subheader("Plano de Contas Atual")
    for conta in sorted(plano, key=lambda x: x["codigo"]):
        st.markdown(f"- **{conta['codigo']}** – {conta['nome']}  `({conta['tipo']})`")
else:
    st.warning("Nenhuma conta encontrada ou arquivo inválido.")
