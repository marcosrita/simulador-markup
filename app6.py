import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Simulador de Markup", layout="wide")

# Título do aplicativo
st.title("📊 Simulador de Markup e Lucro")

# Função para salvar CSV
def salvar_csv(df, nome_arquivo="dados_simulacao.csv"):
    df.to_csv(nome_arquivo, index=False)
    return nome_arquivo

# Função para carregar CSV
def carregar_csv(arquivo):
    return pd.read_csv(arquivo)

# Seção para upload e carregamento de arquivos CSV
st.markdown("### 📂 Carregue um arquivo CSV")
arquivo = st.file_uploader("Escolha um arquivo", type="csv", label_visibility="collapsed")
if arquivo is not None:
    df = carregar_csv(arquivo)
    st.success("Arquivo carregado com sucesso!")
else:
    # Criando um DataFrame vazio como base
    df = pd.DataFrame(columns=["Produto", "Preço de Venda", "Custo", "Markup", "Lucro"])

# Seção de entrada de dados
st.sidebar.header("Cadastro de Produtos")
produto = st.sidebar.text_input("Nome do Produto")
preco_venda = st.sidebar.number_input("Preço de Venda", min_value=0.0, format="%.2f")
custo = st.sidebar.number_input("Custo", min_value=0.0, format="%.2f")

if st.sidebar.button("Adicionar Produto"):
    if produto and preco_venda and custo:
        markup = round(preco_venda / custo, 2) if custo > 0 else 0
        lucro = round(preco_venda - custo, 2)
        novo_dado = pd.DataFrame([[produto, preco_venda, custo, markup, lucro]],
                                 columns=["Produto", "Preço de Venda", "Custo", "Markup", "Lucro"])
        df = pd.concat([df, novo_dado], ignore_index=True)
        st.success(f"{produto} adicionado com sucesso!")
    else:
        st.warning("Preencha todos os campos antes de adicionar um produto.")

# Exibição dos dados cadastrados
st.subheader("📋 Produtos Cadastrados")
st.dataframe(df, use_container_width=True)

# Botão para salvar o arquivo CSV
if st.button("💾 Salvar Projeto"):
    nome_arquivo = salvar_csv(df)
    st.success(f"Arquivo salvo como {nome_arquivo}")
    st.download_button(
        label="📥 Baixar CSV",
        data=open(nome_arquivo, "rb"),
        file_name="dados_simulacao.csv",
        mime="text/csv"
    )

# Gráfico de rentabilidade
if not df.empty:
    st.subheader("📈 Gráfico de Rentabilidade")
    fig = px.bar(df, x="Produto", y="Lucro", text_auto=True, title="Lucro por Produto")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Adicione produtos para visualizar o gráfico.")
