import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import os

st.set_page_config(page_title="Simulador de Markup - Marcos Rita + IA", layout="wide", initial_sidebar_state="expanded")
st.title("Simulador de Markup e Rentabilidade")

menu = st.sidebar.radio("Navegar para:", ["Simulador", "Gráfico de Rentabilidade", "Custos e Relatório PDF"])

if menu == "Simulador":
    st.markdown("## Cadastro de Produtos")
    num_produtos = st.number_input("Quantos produtos deseja cadastrar?", min_value=1, value=3)

    produtos = []
    for i in range(int(num_produtos)):
        with st.expander(f"Produto {i+1}"):
            nome = st.text_input(f"Nome do Produto {i+1}", key=f"nome_{i}")
            preco_venda = st.number_input(f"Preço de Venda (R$) - Produto {i+1}", key=f"venda_{i}")
            custo = st.number_input(f"Custo (R$) - Produto {i+1}", key=f"custo_{i}")
            lucro = preco_venda - custo
            markup = preco_venda / custo if custo else 0
            produtos.append({"Produto": nome, "Preco Venda": preco_venda, "Custo": custo, "Lucro": lucro, "Markup": markup})

    df = pd.DataFrame(produtos)

    if not df.empty:
        st.markdown("### Tabela de Produtos")
        st.dataframe(df, use_container_width=True)

if menu == "Gráfico de Rentabilidade":
    st.markdown("## Gráfico de Rentabilidade")
    if 'df' in locals() and not df.empty:
        st.markdown("## Gráfico de Lucro por Produto")
        fig = px.bar(df, x="Produto", y="Lucro", color="Produto", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## Gráfico de Markup")
        fig2 = px.bar(df, x="Produto", y="Markup", color="Produto", text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Cadastre os produtos primeiro na aba Simulador.")

if menu == "Custos e Relatório PDF":
    st.markdown("## Custos Variáveis")
    num_var = st.number_input("Quantos custos variáveis?", min_value=1, value=3, key="var")
    variaveis = []
    for i in range(int(num_var)):
        nome = st.text_input(f"Nome do Custo Variável {i+1}", key=f"cv_nome_{i}")
        valor = st.number_input(f"Valor R$ - {nome}", key=f"cv_valor_{i}")
        variaveis.append({"Nome": nome, "Valor": valor})
    df_cv = pd.DataFrame(variaveis)

    st.markdown("## Custos Fixos")
    num_fix = st.number_input("Quantos custos fixos?", min_value=1, value=3, key="fix")
    fixos = []
    for i in range(int(num_fix)):
        nome = st.text_input(f"Nome do Custo Fixo {i+1}", key=f"cf_nome_{i}")
        valor = st.number_input(f"Valor R$ - {nome}", key=f"cf_valor_{i}")
        fixos.append({"Nome": nome, "Valor": valor})
    df_cf = pd.DataFrame(fixos)

    if not df.empty:
        lucro_total = df["Lucro"].sum()
        markup_medio = df["Markup"].mean()

        if st.button("Gerar Relatório PDF"):
            def gerar_relatorio_pdf(df_produtos, df_custos_variaveis, df_custos_fixos, lucro_total, markup_medio):
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
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
                for _, row in df_custos_variaveis.iterrows():
                    pdf.cell(0, 8, f'{row["Nome"]}: R${row["Valor"]:.2f}', ln=True)
                pdf.ln(5)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "Custos Fixos", ln=True)
                pdf.set_font("Arial", "", 10)
                for _, row in df_custos_fixos.iterrows():
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

            caminho = gerar_relatorio_pdf(df, df_cv, df_cf, lucro_total, markup_medio)
            with open(caminho, "rb") as file:
                st.download_button("📄 Baixar Relatório PDF", file, file_name="relatorio_simulador.pdf")
