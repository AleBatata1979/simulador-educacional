import streamlit as st
import json
import os

st.title("📉 Demonstração do Resultado do Exercício (DRE)")

DATA_PATH = "data/lancamentos.json"

def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

# Agrupamento por categorias
CATEGORIAS = {
    "Receita de Vendas": "Receita Operacional",
    "Custo das Mercadorias Vendidas": "Custo das Vendas",
    "Despesas Administrativas": "Despesas Operacionais",
    "Salários": "Despesas Operacionais",
    "Aluguel": "Despesas Operacionais"
}

valores = {
    "Receita Operacional": 0,
    "Custo das Vendas": 0,
    "Despesas Operacionais": 0
}

lancamentos = carregar_lancamentos()

for l in lancamentos:
    conta = l["credito"]
    valor = l["valor"]
    if conta in CATEGORIAS:
        categoria = CATEGORIAS[conta]
        valores[categoria] += valor

    conta = l["debito"]
    if conta in CATEGORIAS:
        categoria = CATEGORIAS[conta]
        valores[categoria] -= valor

# Cálculo
receita = valores["Receita Operacional"]
custo = valores["Custo das Vendas"]
despesas = valores["Despesas Operacionais"]
lucro_bruto = receita - custo
lucro_liquido = lucro_bruto - despesas

# Exibição
st.markdown("### Resultado Resumido")
st.write(f"**Receita Operacional:** R$ {receita:,.2f}")
st.write(f"**(-) Custo das Vendas:** R$ {custo:,.2f}")
st.write(f"**= Lucro Bruto:** R$ {lucro_bruto:,.2f}")
st.write(f"**(-) Despesas Operacionais:** R$ {despesas:,.2f}")
st.success(f"**= Lucro Líquido:** R$ {lucro_liquido:,.2f}")
