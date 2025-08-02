
import streamlit as st
import json
from pathlib import Path
from datetime import date

st.title("🧾 Lançamentos Contábeis")

DATA_PATH = Path("data/lancamentos.json")

def carregar_lancamentos():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

def salvar_lancamento(lancamento):
    dados = carregar_lancamentos()
    dados.append(lancamento)
    with open(DATA_PATH, "w") as f:
        json.dump(dados, f, indent=2)

with st.form("form_lancamento"):
    data = st.date_input("Data", value=date.today())
    conta_debito = st.text_input("Conta Débito")
    conta_credito = st.text_input("Conta Crédito")
    valor = st.number_input("Valor", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Lançar")

    if submitted:
        salvar_lancamento({
            "data": data.strftime("%Y-%m-%d"),
            "conta_debito": conta_debito,
            "conta_credito": conta_credito,
            "valor": valor
        })
        st.success("Lançamento registrado com sucesso!")

st.divider()
st.subheader("📜 Lançamentos Registrados")
for lanc in carregar_lancamentos():
    st.write(f"{lanc['data']} | Débito: {lanc['conta_debito']} | Crédito: {lanc['conta_credito']} | R$ {float(lanc['valor']):,.2f}")
