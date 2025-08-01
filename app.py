import streamlit as st

st.set_page_config(page_title="Simulador Educacional", layout="wide")

st.sidebar.title("📘 Menu")
st.sidebar.page_link("app.py", label="🏠 Início", icon="🏠")
st.sidebar.page_link("pages/1_Balanco.py", label="📊 Balanço Patrimonial", icon="📈")

st.title("🧮 Simulador Educacional Integrado")
st.write("""
Bem-vindo! Escolha uma opção no menu à esquerda para começar.
Este simulador foi criado para te ajudar a aplicar conceitos de contabilidade, finanças, estatística e análise de projetos.
""")
