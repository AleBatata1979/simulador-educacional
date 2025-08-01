import streamlit as st
import pandas as pd

st.title("📊 Simulador de Balanço Patrimonial")

st.subheader("Insira os valores do seu balanço:")

with st.form("balanco_form"):
    st.markdown("### Ativo")
    ativo_circulante = st.number_input("Ativo Circulante", value=0.0)
    ativo_nao_circulante = st.number_input("Ativo Não Circulante", value=0.0)

    st.markdown("### Passivo")
    passivo_circulante = st.number_input("Passivo Circulante", value=0.0)
    passivo_nao_circulante = st.number_input("Passivo Não Circulante", value=0.0)

    st.markdown("### Patrimônio Líquido")
    patrimonio_liquido = st.number_input("Patrimônio Líquido", value=0.0)

    submitted = st.form_submit_button("Verificar Balanço")

if submitted:
    total_ativo = ativo_circulante + ativo_nao_circulante
    total_passivo = passivo_circulante + passivo_nao_circulante + patrimonio_liquido

    st.markdown("## Resultado:")
    col1, col2 = st.columns(2)
    col1.metric("Total Ativo", f"R$ {total_ativo:,.2f}")
    col2.metric("Passivo + PL", f"R$ {total_passivo:,.2f}")

    if total_ativo == total_passivo:
        st.success("✅ O balanço está equilibrado!")
    else:
        st.error("❌ O balanço está desequilibrado. Verifique os valores inseridos.")
