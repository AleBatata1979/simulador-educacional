import streamlit as st
import json
import os

st.title("📉 Demonstração do Resultado do Exercício (DRE)")

DATA_PATH = "data/lancamentos.json"
PLANO_PATH = "data/plano_contas.json"

@st.cache_data
def carregar_lancamentos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@st.cache_data
def carregar_plano():
    if os.path.exists(PLANO_PATH):
        with open(PLANO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

lancamentos = carregar_lancamentos()
plano = carregar_plano()

# Variações simuladas
receita_var = st.slider("Variação da Receita (%)", -50, 50, 0)
custo_var = st.slider("Variação do Custo (%)", -50, 50, 0)
despesa_var = st.slider("Variação das Despesas Operacionais (%)", -50, 50, 0)
ir_percentual = st.slider("Percentual de IR e Contribuições (%)", 0, 30, 18)

# Saldos por tipo de conta
saldos = {}
for lanc in lancamentos:
    debito = lanc["conta_debito"]
    credito = lanc["conta_credito"]
    valor = float(lanc["valor"])
    saldos[debito] = saldos.get(debito, 0) + valor
    saldos[credito] = saldos.get(credito, 0) - valor

# Agregar contas
def obter(conta):
    return sum(v for k, v in saldos.items() if conta.lower() in k.lower())

receita_bruta = obter("Receita de Vendas")
deducoes = 0
receita_liquida = receita_bruta - deducoes
cmv = abs(obter("Custo das Mercadorias Vendidas"))
lucro_bruto = receita_liquida - cmv

# Despesas Operacionais
desp_admin = abs(obter("Despesas Administrativas"))
salarios = abs(obter("Salários"))
aluguel = abs(obter("Aluguel"))
despesas_op = desp_admin + salarios + aluguel

resultado_operacional = lucro_bruto - despesas_op

outras_receitas = abs(obter("Outras Receitas"))
outras_despesas = abs(obter("Outras Despesas"))
resultado_antes_ir = resultado_operacional + outras_receitas - outras_despesas

ir = resultado_antes_ir * (ir_percentual / 100)
lucro_liquido = resultado_antes_ir - ir

st.subheader("🧾 Resultado Resumido")

def formatar(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.markdown(f"""
**Receita Bruta:** {formatar(receita_bruta)}

(-) Deduções: {formatar(deducoes)}

= **Receita Líquida:** {formatar(receita_liquida)}

(-) Custo das Mercadorias Vendidas: {formatar(cmv)}

= **Lucro Bruto:** {formatar(lucro_bruto)}

(-) Despesas Operacionais:  
 - Administrativas: {formatar(desp_admin)}  
 - Salários: {formatar(salarios)}  
 - Aluguel: {formatar(aluguel)}  

= **Resultado Operacional:** {formatar(resultado_operacional)}

(+) Outras Receitas: {formatar(outras_receitas)}  
(-) Outras Despesas: {formatar(outras_despesas)}  

= **Resultado Antes do IR:** {formatar(resultado_antes_ir)}

(-) IR e Contribuições ({ir_percentual}%): {formatar(ir)}

💰 **Lucro Líquido do Exercício:** {formatar(lucro_liquido)}
""")
