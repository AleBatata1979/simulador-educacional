import streamlit as st
import json
import os

st.title("📊 Cenários de Sensibilidade")

DATA_PATH = "data/lancamentos.json"

# Categorias sensíveis
CATEGORIAS = {
    "Receita de Vendas": "Receita",
    "Custo das Mercadorias Vendidas": "Custo",
    "Despesas Administrativas": "Despesa",
    "Salários": "Despesa",
    "Aluguel": "Despesa"
}

def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

# Slider de variações
st.sidebar.header("🔧 Ajustes de Cenário")
fatores = {
    "Receita de Vendas": st.sidebar.slider("Variação da Receita (%)", -50, 50, 0),
    "Custo das Mercadorias Vendidas": st.sidebar.slider("Variação do Custo (%)", -50, 50, 0),
    "Despesas Administrativas": st.sidebar.slider("Variação das Despesas Administrativas (%)", -50, 50, 0),
    "Salários": st.sidebar.slider("Variação dos Salários (%)", -50, 50, 0),
    "Aluguel": st.sidebar.slider("Variação do Aluguel (%)", -50, 50, 0)
}

# Processamento
lancamentos = carregar_lancamentos()
valores_base = {"Receita": 0, "Custo": 0, "Despesa": 0}
valores_novo = {"Receita": 0, "Custo": 0, "Despesa": 0}

for l in lancamentos:
    for tipo in ["debito", "credito"]:
        conta = l[tipo]
        valor = l["valor"]
        if conta in CATEGORIAS:
            categoria = CATEGORIAS[conta]
            sinal = 1 if tipo == "credito" else -1
            valores_base[categoria] += sinal * valor

            ajuste = 1 + (fatores.get(conta, 0) / 100)
            valores_novo[categoria] += sinal * valor * ajuste

def dre(val):
    receita = val["Receita"]
    custo = val["Custo"]
    desp = val["Despesa"]
    bruto = receita - custo
    liquido = bruto - desp
    return receita, custo, desp, bruto, liquido

r1 = dre(valores_base)
r2 = dre(valores_novo)

st.markdown("### 💼 DRE - Cenário Atual")
st.write(f"Receita: R$ {r1[0]:,.2f} | Custo: R$ {r1[1]:,.2f} | Despesa: R$ {r1[2]:,.2f}")
st.success(f"Lucro Líquido: R$ {r1[4]:,.2f}")

st.markdown("---")

st.markdown("### 🔄 DRE - Cenário Ajustado")
st.write(f"Receita: R$ {r2[0]:,.2f} | Custo: R$ {r2[1]:,.2f} | Despesa: R$ {r2[2]:,.2f}")
st.success(f"Lucro Líquido: R$ {r2[4]:,.2f}")
