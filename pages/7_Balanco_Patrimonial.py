import streamlit as st
import json
import os

st.title("📄 Balanço Patrimonial")

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

def extrair_contas(plano):
    contas = {}
    for grupo, dados in plano.items():
        tipo = dados.get("tipo", "")
        subcontas = dados.get("subcontas", {})
        for s1, d1 in subcontas.items():
            subtipo = d1.get("tipo", "")
            for s2 in d1.get("subcontas", {}).keys():
                contas[s2] = {"grupo": grupo, "tipo": tipo or subtipo}
    return contas

lancamentos = carregar_lancamentos()
plano = carregar_plano()
contas_info = extrair_contas(plano)

saldos = {}
for lanc in lancamentos:
    conta_debito = lanc["conta_debito"]
    conta_credito = lanc["conta_credito"]
    valor = float(lanc["valor"])

    saldos[conta_debito] = saldos.get(conta_debito, 0) + valor
    saldos[conta_credito] = saldos.get(conta_credito, 0) - valor

# Separar por tipo
ativos = {}
passivos = {}
pl = {}

for conta, saldo in saldos.items():
    info = contas_info.get(conta)
    if not info:
        continue
    grupo = info["grupo"]
    if grupo.startswith("1."):
        ativos[conta] = saldo
    elif grupo.startswith("2."):
        passivos[conta] = saldo
    elif grupo.startswith("3."):
        pl[conta] = saldo

st.subheader("🔹 Ativo")
for c, v in ativos.items():
    st.write(f"- {c}: R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.subheader("🔸 Passivo")
for c, v in passivos.items():
    st.write(f"- {c}: R$ {abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.subheader("🟢 Patrimônio Líquido")
for c, v in pl.items():
    st.write(f"- {c}: R$ {abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

total_ativo = sum(ativos.values())
total_passivo = sum(abs(v) for v in passivos.values())
total_pl = sum(abs(v) for v in pl.values())

st.markdown("---")
st.subheader("🔄 Verificação")
st.write(f"**Total do Ativo:** R$ {total_ativo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.write(f"**Total do Passivo + PL:** R$ {(total_passivo + total_pl):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

if round(total_ativo, 2) == round(total_passivo + total_pl, 2):
    st.success("✅ O Balanço está equilibrado!")
else:
    st.error("❌ O Balanço NÃO está equilibrado.")
