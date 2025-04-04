import streamlit as st

st.set_page_config(page_title="Simulador de Markup - Marcos Rita + IA", layout="wide")

import home
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import os
import base64

st.title("Simulador de Markup e Rentabilidade")

def gerar_pdf(df_produtos, df_cv, df_cf, lucro_total, markup_medio, meta_lucro):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatório de Rentabilidade", ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, "Marcos Rita + IA", ln=True, align="C")
    pdf.ln(10)

    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, f"Data do relatório: {data_atual}", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Meta de Lucro", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 8, f"Meta de Lucro: R${meta_lucro:.2f}", ln=True)
    pdf.cell(200, 8, f"Lucro Total Estimado: R${lucro_total:.2f}", ln=True)
    atingiu_meta = "Sim" if lucro_total >= meta_lucro else "Não"
    pdf.cell(200, 8, f"Meta Atingida: {atingiu_meta}", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Produtos", ln=True)
    pdf.set_font("Arial", size=10)
    for i, row in df_produtos.iterrows():
        pdf.cell(200, 8, f"{row['Produto']}: Venda=R${row['Preco Venda']:.2f} | Custo=R${row['Custo']:.2f} | Lucro=R${row['Lucro']:.2f} | Markup={row['Markup']:.2f}x", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Custos Variáveis", ln=True)
    pdf.set_font("Arial", size=10)
    for i, row in df_cv.iterrows():
        pdf.cell(200, 8, f"{row['Nome']}: R${row['Valor']:.2f}", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Custos Fixos", ln=True)
    pdf.set_font("Arial", size=10)
    for i, row in df_cf.iterrows():
        pdf.cell(200, 8, f"{row['Nome']}: R${row['Valor']:.2f}", ln=True)

    caminho = os.path.join(os.getcwd(), "relatorio_simulador.pdf")
    pdf.output(caminho)
    return caminho

if 'meta_lucro' not in st.session_state:
    st.session_state['meta_lucro'] = 0.0

menu = st.sidebar.radio("Navegar para:", [
    "Início",
    "Meta de Lucro",
    "Produtos",
    "Custos Variáveis",
    "Custos Fixos",
    "Simulador",
    "Gráfico de Rentabilidade",
    "Relatório/Gráfico",
    "Salvar/Carregar"
])

if menu == "Meta de Lucro":
    st.subheader("Definir Meta de Lucro")
    meta_lucro = st.number_input("Defina a meta de lucro desejada (R$)", min_value=0.0, value=st.session_state['meta_lucro'])
    if st.button("Salvar Meta"):
        st.session_state['meta_lucro'] = meta_lucro
        st.success(f"Meta de lucro definida: R${meta_lucro:.2f}")

elif menu == "Relatório/Gráfico":
    st.subheader("Gráficos e PDF")
    if st.session_state['produtos']:
        df_produtos = pd.DataFrame(st.session_state['produtos'])
        df_cv = pd.DataFrame(st.session_state['custos_variaveis']) if st.session_state['custos_variaveis'] else pd.DataFrame(columns=["Nome", "Valor"])
        df_cf = pd.DataFrame(st.session_state['custos_fixos']) if st.session_state['custos_fixos'] else pd.DataFrame(columns=["Nome", "Valor"])
        lucro_total = df_produtos['Lucro'].sum()
        markup_medio = df_produtos['Markup'].mean()

        st.markdown("### Gráfico de Lucro")
        fig = px.bar(df_produtos, x="Produto", y="Lucro", text_auto=True)
        st.plotly_chart(fig)

        st.markdown("### Gráfico de Markup")
        fig2 = px.bar(df_produtos, x="Produto", y="Markup", text_auto=True)
        st.plotly_chart(fig2)

        st.markdown(f"### Meta de Lucro: R${st.session_state['meta_lucro']:.2f}")
        st.markdown(f"### Lucro Total Estimado: R${lucro_total:.2f}")
        atingiu_meta = "✅ Meta Atingida!" if lucro_total >= st.session_state['meta_lucro'] else "❌ Meta Não Atingida"
        st.markdown(f"## {atingiu_meta}")

        if st.button("📄 Gerar PDF"):
            caminho_pdf = gerar_pdf(df_produtos, df_cv, df_cf, lucro_total, markup_medio, st.session_state['meta_lucro'])
            with open(caminho_pdf, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_simulador.pdf">📥 Baixar PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

st.sidebar.markdown("Versão: Marcos Rita + IA")
