import streamlit as st
import json
import os

st.title("📚 Plano de Contas")

file_path = "data/plano_contas.json"

def carregar_plano():
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def mostrar_plano(plano, nivel=0):
    for conta, subcontas in plano.items():
        st.markdown(" " * nivel * 4 + f"- **{conta}**")
        if isinstance(subcontas, dict) and subcontas:
            mostrar_plano(subcontas, nivel + 1)

if os.path.exists(file_path):
    plano = carregar_plano()
    mostrar_plano(plano)
else:
    st.error("Plano de contas não encontrado.")
