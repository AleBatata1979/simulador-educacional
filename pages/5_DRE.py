import streamlit as st
import json
import os

st.title("📉 Demonstração do Resultado do Exercício (DRE)")

DATA_PATH = "data/lancamentos.json"

# Categorias
RECEITAS = ["Receita de Vendas"]
CUSTOS = ["Custo das Mercadorias Vendidas"]
DESPESAS_ADMIN = ["Despesas Administrativas"]
SALARIOS = ["Salários"]
ALUGUEL = ["Aluguel"]
OUTRAS_RECEITAS = ["Outras Receitas"]
OUTRAS_DESPESAS = ["Outras Despesas"]

def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

# IR
st.sidebar.header("⚙️ Parâmetros")
ir_percentual = st.sidebar.slider("Alíquota de IR e Contribuições (%)", 0, 50, 15)

lancamentos = carregar_lancamentos()
saldos = {
    "receita_bruta": 0,
    "deducoes": 0,
    "cmv": 0,
    "admin": 0,
    "salarios": 0,
    "aluguel": 0,
    "outras_receitas": 0,
    "outras_despesas": 0
}

for l in lancamentos:
    for tipo in ["debito", "credito"]:
        conta = l[tipo]
        valor = l["valor"]
        sinal = 1 if tipo == "credito" else -1

        if conta in RECEITAS:
            saldos["receita_bruta"] += sinal * valor
        elif conta in CUSTOS:
            saldos["cmv"] += sinal * valor
        elif conta in DESPESAS_ADMIN:
            saldos["admin"] += sinal * valor
        elif conta in SALARIOS:
            saldos["salarios"] += sinal * valor
        elif conta in ALUGUEL:
            saldos["aluguel"] += sinal * valor
        elif conta in OUTRAS_RECEITAS:
            saldos["outras_receitas"] += sinal * valor
        elif conta in OUTRAS_DESPESAS:
            saldos["outras_despesas"] += sinal * valor

# Cálculos
receita_liquida = saldos["receita_bruta"] - saldos["deducoes"]
lucro_bruto = receita_liquida - saldos["cmv"]
despesas_op = saldos["admin"] + saldos["salarios"] + saldos["aluguel"]
resultado_operacional = lucro_bruto - despesas_op
resultado_antes_ir = resultado_operacional + saldos["outras_receitas"] - saldos["outras_despesas"]
ir_valor = resultado_antes_ir * (ir_percentual / 100) if resultado_antes_ir > 0 else 0
lucro_liquido = resultado_antes_ir - ir_valor

# Exibição
st.markdown("### 🧾 Resultado Resumido")
st.write(f"**Receita Bruta:** R$ {saldos['receita_bruta']:,.2f}")
st.write(f"**(-) Deduções:** R$ {saldos['deducoes']:,.2f}")
st.write(f"**= Receita Líquida:** R$ {receita_liquida:,.2f}")
st.write(f"**(-) Custo das Mercadorias Vendidas:** R$ {saldos['cmv']:,.2f}")
st.write(f"**= Lucro Bruto:** R$ {lucro_bruto:,.2f}")
st.write("**(-) Despesas Operacionais:**")
st.write(f"&emsp;- Administrativas: R$ {saldos['admin']:,.2f}")
st.write(f"&emsp;- Salários: R$ {saldos['salarios']:,.2f}")
st.write(f"&emsp;- Aluguel: R$ {saldos['aluguel']:,.2f}")
st.write(f"**= Resultado Operacional:** R$ {resultado_operacional:,.2f}")
st.write(f"**(+) Outras Receitas:** R$ {saldos['outras_receitas']:,.2f}")
st.write(f"**(-) Outras Despesas:** R$ {saldos['outras_despesas']:,.2f}")
st.write(f"**= Resultado Antes do IR:** R$ {resultado_antes_ir:,.2f}")
st.write(f"**(-) IR e Contribuições ({ir_percentual}%):** R$ {ir_valor:,.2f}")
st.success(f"💰 Lucro Líquido do Exercício: R$ {lucro_liquido:,.2f}")
