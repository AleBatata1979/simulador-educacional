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

TIPOS_CONTAS = {
    "Caixa": "Ativo", "Bancos": "Ativo", "Clientes": "Ativo", "Estoques": "Ativo",
    "Fornecedores": "Passivo", "Empréstimos": "Passivo", "Capital Social": "Patrimônio Líquido",
    "Receita de Vendas": "Receita", "Custo das Mercadorias Vendidas": "Despesa",
    "Despesas Administrativas": "Despesa", "Salários": "Despesa", "Aluguel": "Despesa"
}

def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

def salvar_lancamento(lancamento):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    lancamentos = carregar_lancamentos()
    lancamentos.append(lancamento)
    with open(DATA_PATH, "w") as f:
        json.dump(lancamentos, f, indent=4)

def excluir_lancamento(index):
    lancamentos = carregar_lancamentos()
    if 0 <= index < len(lancamentos):
        lancamentos.pop(index)
        with open(DATA_PATH, "w") as f:
            json.dump(lancamentos, f, indent=4)

with st.form("form_lancamento"):
    data = st.date_input("Data", value=datetime.today())
    conta_debito = st.selectbox("Conta Débito", PLAN_CONTAS)
    conta_credito = st.selectbox("Conta Crédito", PLAN_CONTAS)
    valor = st.number_input("Valor", min_value=0.01, step=0.01)
    submit = st.form_submit_button("Lançar")

if submit:
    erros = []
    if TIPOS_CONTAS[conta_debito] == "Receita":
        erros.append("❌ Receita não deve ser usada no débito.")
    if TIPOS_CONTAS[conta_credito] in ["Despesa", "Custo"]:
        erros.append("❌ Custo e Despesa não devem ser usadas no crédito.")

    if erros:
        for e in erros:
            st.error(e)
    else:
        salvar_lancamento({
            "data": data.strftime("%Y-%m-%d"),
            "debito": conta_debito,
            "credito": conta_credito,
            "valor": valor
        })
        st.success("✅ Lançamento registrado com sucesso!")

st.subheader("📜 Lançamentos Registrados")
lancamentos = carregar_lancamentos()
for i, l in enumerate(lancamentos):
    col1, col2 = st.columns([4,1])
    with col1:
        st.write(f"{l['data']} | Débito: {l['debito']} | Crédito: {l['credito']} | R$ {l['valor']:.2f}")
    with col2:
        if st.button("🗑️ Excluir", key=f"del_{i}"):
            excluir_lancamento(i)
            st.experimental_rerun()
