import streamlit as st
import json
from datetime import datetime
import os

st.title("🧾 Lançamentos Contábeis")

DATA_PATH = "data/lancamentos.json"
PLAN_CONTAS = [
    "Caixa", "Bancos", "Clientes", "Estoques",
    "Fornecedores", "Empréstimos", "Capital Social",
    "Receita de Vendas", "Custo das Mercadorias Vendidas",
    "Despesas Administrativas", "Salários", "Aluguel"
]

def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

def salvar_lancamento(lancamento):
    lancamentos = carregar_lancamentos()
    lancamentos.append(lancamento)
    with open(DATA_PATH, "w") as f:
        json.dump(lancamentos, f, indent=4)

with st.form("form_lancamento"):
    data = st.date_input("Data", value=datetime.today())
    conta_debito = st.selectbox("Conta Débito", PLAN_CONTAS)
    conta_credito = st.selectbox("Conta Crédito", PLAN_CONTAS)
    valor = st.number_input("Valor", min_value=0.01, step=0.01)
    submit = st.form_submit_button("Lançar")

if submit:
    salvar_lancamento({
        "data": data.strftime("%Y-%m-%d"),
        "debito": conta_debito,
        "credito": conta_credito,
        "valor": valor
    })
    st.success("✅ Lançamento registrado com sucesso!")

st.subheader("📜 Lançamentos Registrados")
for l in carregar_lancamentos():
    st.write(f"{l['data']} | Débito: {l['debito']} | Crédito: {l['credito']} | R$ {l['valor']:.2f}")
