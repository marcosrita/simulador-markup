import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import os

st.set_page_config(page_title="Simulador de Markup - Marcos Rita +IA", layout="wide", initial_sidebar_state="expanded")
st.title("Simulador de Markup e Rentabilidade")

# Menu lateral
menu = st.sidebar.radio("Navegar para:", ["Simulador", "Gráfico de Rentabilidade"])

if menu == "Simulador":
    st.markdown("## Cadastro de Produtos")
    st.markdown("### Carregar projeto salvo (.csv)")
    uploaded_file = st.file_uploader("Arraste e solte o arquivo aqui", type=["csv"], help="Limite: 200MB por arquivo • CSV")
    
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
