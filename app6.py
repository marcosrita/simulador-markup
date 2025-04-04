import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import os

st.set_page_config(page_title="Simulador de Markup - Marcos Rita + IA", layout="wide", initial_sidebar_state="expanded")
st.title("Simulador de Markup e Rentabilidade")

# Menu lateral
menu = st.sidebar.radio("Navegar para:", ["Simulador", "Gráfico de Rentabilidade"])

# Funções auxiliares para salvar e carregar CSV

def salvar_csv(df, nome_arquivo):
    df.to_csv(nome_arquivo, index=False)
    with open(nome_arquivo, "rb") as file:
        st.download_button(
            label="📥 Baixar dados como CSV",
            data=file,
            file_name=nome_arquivo,
            mime="text/csv"
        )

def carregar_csv(uploaded_file):
    return pd.read_csv(uploaded_file) if uploaded_file is not None else pd.DataFrame()

if menu == "Simulador":
    st.markdown("## Cadastro de Produtos")

    uploaded_file = st.file_uploader("🔄 Carregar projeto salvo (.csv)", type="csv")
    df = carregar_csv(uploaded_file)

    if df.empty:
        num_produtos = st.number_input("Quantos produtos deseja cadastrar?", min_value=1, value=3)

        produtos = []
        for i in range(int(num_produtos)):
            with st.expander(f"Produto {i+1}"):
                nome = st.text_input(f"Nome do Produto {i+1}", key=f"nome_{i}")
                preco_venda = st.number_input(f"Preço de Venda (R$) - Produto {i+1}", key=f"venda_{i}")
                custo = st.number_input(f"Custo (R$) - Produto {i+1}", key=f"custo_{i}")
                produtos.append({"Produto": nome, "Preço de Venda": preco_venda, "Custo": custo})

        df = pd.DataFrame(produtos)

    if not df.empty:
        st.markdown("### Tabela de Produtos")
        st.dataframe(df, use_container_width=True)

        # Botão para salvar CSV
        salvar_csv(df, "projeto_simulador.csv")

elif menu == "Gráfico de Rentabilidade":
    st.markdown("## Cadastro de Produtos para Gráfico")
    num_produtos = st.number_input("Quantos produtos deseja analisar?", min_value=1, value=3, key="grafico_num")

    data = []
    for i in range(int(num_produtos)):
        with st.expander(f"Produto {i+1} - Gráfico"):
            nome = st.text_input(f"Nome do Produto {i+1} (Gráfico)", key=f"g_nome_{i}")
            preco_venda = st.number_input(f"Preço de Venda (R$) - Produto {i+1} (Gráfico)", key=f"g_venda_{i}")
            custo_total = st.number_input(f"Custo Total (R$) - Produto {i+1} (Gráfico)", key=f"g_custo_{i}")
            lucro = preco_venda - custo_total
            margem = (lucro / preco_venda) * 100 if preco_venda else 0
            data.append({
                "Produto": nome,
                "Preço de Venda (R$)": preco_venda,
                "Custo Total (R$)": custo_total,
                "Lucro (R$)": lucro,
                "Margem de Lucro (%)": margem
            })

    df_grafico = pd.DataFrame(data)

    if not df_grafico.empty:
        st.markdown("## Tabela de Rentabilidade")
        st.dataframe(df_grafico, use_container_width=True)

        st.markdown("## Gráfico de Lucro por Produto")
        fig = px.bar(df_grafico, x="Produto", y="Lucro (R$)", color="Produto", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## Gráfico de Margem de Lucro (%)")
        fig2 = px.bar(df_grafico, x="Produto", y="Margem de Lucro (%)", color="Produto", text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Preencha os dados para visualizar os gráficos.")
