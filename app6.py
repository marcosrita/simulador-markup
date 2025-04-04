import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import os

st.set_page_config(page_title="Simulador de Markup - Marcos Rita + IA", layout="wide", initial_sidebar_state="expanded")
st.title("Simulador de Markup e Rentabilidade")

# Menu lateral
menu = st.sidebar.radio("Navegar para:", ["Simulador", "Gráfico de Rentabilidade", "Relatório PDF"])

# Sessão de cadastro de produtos
if menu == "Simulador":
    st.subheader("Cadastro de Produtos")
    num_produtos = st.number_input("Quantos produtos deseja cadastrar?", min_value=1, value=3)

    produtos = []
    for i in range(int(num_produtos)):
        with st.expander(f"Produto {i+1}"):
            nome = st.text_input(f"Nome do Produto {i+1}", key=f"nome_{i}")
            preco_venda = st.number_input(f"Preço de Venda (R$) - Produto {i+1}", key=f"venda_{i}")
            custo = st.number_input(f"Custo (R$) - Produto {i+1}", key=f"custo_{i}")
            markup = preco_venda / custo if custo else 0
            lucro = preco_venda - custo
            produtos.append({"Produto": nome, "Preco Venda": preco_venda, "Custo": custo, "Markup": markup, "Lucro": lucro})

    if produtos:
        df = pd.DataFrame(produtos)
        st.markdown("### Tabela de Produtos")
        st.dataframe(df, use_container_width=True)

        # Custos Variáveis
        st.subheader("Custos Variáveis")
        custos_variaveis = []
        num_variaveis = st.number_input("Quantos tipos de custos variáveis?", min_value=0, value=2)
        for i in range(int(num_variaveis)):
            nome = st.text_input(f"Nome do Custo Variável {i+1}", key=f"cv_nome_{i}")
            valor = st.number_input(f"Valor (R$) - Custo Variável {i+1}", key=f"cv_valor_{i}")
            custos_variaveis.append({"Nome": nome, "Valor": valor})

        df_cv = pd.DataFrame(custos_variaveis)
        st.dataframe(df_cv)

        # Custos Fixos
        st.subheader("Custos Fixos")
        custos_fixos = []
        num_fixos = st.number_input("Quantos tipos de custos fixos?", min_value=0, value=2)
        for i in range(int(num_fixos)):
            nome = st.text_input(f"Nome do Custo Fixo {i+1}", key=f"cf_nome_{i}")
            valor = st.number_input(f"Valor (R$) - Custo Fixo {i+1}", key=f"cf_valor_{i}")
            custos_fixos.append({"Nome": nome, "Valor": valor})

        df_cf = pd.DataFrame(custos_fixos)
        st.dataframe(df_cf)

# Sessão de gráficos
elif menu == "Gráfico de Rentabilidade":
    st.subheader("Gráfico de Rentabilidade")
    num_grafico = st.number_input("Quantos produtos deseja analisar?", min_value=1, value=3, key="grafico")
    data_grafico = []

    for i in range(int(num_grafico)):
        with st.expander(f"Produto {i+1} - Gráfico"):
            nome = st.text_input(f"Nome do Produto {i+1} (Gráfico)", key=f"gnome_{i}")
            venda = st.number_input(f"Preço de Venda (R$)", key=f"gvenda_{i}")
            custo = st.number_input(f"Custo Total (R$)", key=f"gcusto_{i}")
            lucro = venda - custo
            margem = (lucro / venda) * 100 if venda else 0
            data_grafico.append({"Produto": nome, "Lucro (R$)": lucro, "Margem de Lucro (%)": margem})

    df_grafico = pd.DataFrame(data_grafico)

    if not df_grafico.empty:
        st.dataframe(df_grafico)
        fig1 = px.bar(df_grafico, x="Produto", y="Lucro (R$)", color="Produto", text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.bar(df_grafico, x="Produto", y="Margem de Lucro (%)", color="Produto", text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)

# Sessão de PDF
elif menu == "Relatório PDF":
    st.subheader("Gerar Relatório PDF")

    if 'df' in locals():
        lucro_total = df['Lucro'].sum()
        markup_medio = df['Markup'].mean()

        def gerar_relatorio_pdf(df_produtos, df_custos_variaveis, df_custos_fixos, lucro_total, markup_medio):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Relatório de Rentabilidade", ln=True, align="C")
            pdf.set_font("Arial", "I", 12)
            pdf.cell(0, 10, "Marcos Rita + IA", ln=True, align="C")
            pdf.ln(10)

            data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 10, f"Data do relatório: {data_atual}", ln=True)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Produtos", ln=True)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(40, 8, "Nome", border=1)
            pdf.cell(30, 8, "Venda", border=1)
            pdf.cell(30, 8, "Custo", border=1)
            pdf.cell(30, 8, "Markup", border=1)
            pdf.cell(30, 8, "Lucro", border=1)
            pdf.ln()

            pdf.set_font("Arial", "", 10)
            for _, row in df_produtos.iterrows():
                pdf.cell(40, 8, str(row["Produto"]), border=1)
                pdf.cell(30, 8, f'R${row["Preco Venda"]:.2f}', border=1)
                pdf.cell(30, 8, f'R${row["Custo"]:.2f}', border=1)
                pdf.cell(30, 8, f'{row["Markup"]:.2f}x', border=1)
                pdf.cell(30, 8, f'R${row["Lucro"]:.2f}', border=1)
                pdf.ln()

            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Custos Variáveis", ln=True)
            pdf.set_font("Arial", "", 10)
            for _, row in df_cv.iterrows():
                pdf.cell(0, 8, f'{row["Nome"]}: R${row["Valor"]:.2f}', ln=True)

            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Custos Fixos", ln=True)
            pdf.set_font("Arial", "", 10)
            for _, row in df_cf.iterrows():
                pdf.cell(0, 8, f'{row["Nome"]}: R${row["Valor"]:.2f}', ln=True)

            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Resumo Financeiro", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 8, f"Lucro total estimado: R${lucro_total:.2f}", ln=True)
            pdf.cell(0, 8, f"Markup médio: {markup_medio:.2f}x", ln=True)

            caminho_pdf = os.path.join(os.getcwd(), "relatorio_simulador.pdf")
            pdf.output(caminho_pdf)
            return caminho_pdf

        if st.button("Gerar Relatório PDF"):
            caminho = gerar_relatorio_pdf(df, df_cv, df_cf, lucro_total, markup_medio)
            st.success(f"Relatório gerado com sucesso: {caminho}")
            with open(caminho, "rb") as f:
                st.download_button("Baixar PDF", f, file_name="relatorio_simulador.pdf")
    else:
        st.warning("Cadastre produtos na aba 'Simulador' antes de gerar o PDF.")
