import streamlit as st
import pandas as pd
import plotly.express as px
import base64

def salvar_csv(df, filename="dados.csv"):
    csv = df.to_csv(index=False, sep=';')
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Baixar CSV</a>'
    return href

def carregar_csv(uploaded_file):
    return pd.read_csv(uploaded_file, sep=';')

st.set_page_config(page_title="Simulador de Markup", layout="wide")
st.title("📊 Simulador de Markup e Lucro")

# Carregar arquivo CSV
st.subheader("Carregar dados salvos")
uploaded_file = st.file_uploader("Arraste e solte o arquivo aqui", type=["csv"])

df = pd.DataFrame(columns=["Produto", "Preço de Venda", "Custo Variável", "Custo Fixo", "Lucro"])

if uploaded_file is not None:
    df = carregar_csv(uploaded_file)
    st.success("Arquivo carregado com sucesso!")

# Cadastro de produtos
st.subheader("Cadastro de Produtos")
col1, col2, col3, col4 = st.columns(4)
with col1:
    produto = st.text_input("Produto")
with col2:
    preco_venda = st.number_input("Preço de Venda", min_value=0.0, format="%.2f")
with col3:
    custo_variavel = st.number_input("Custo Variável", min_value=0.0, format="%.2f")
with col4:
    custo_fixo = st.number_input("Custo Fixo", min_value=0.0, format="%.2f")

if st.button("Adicionar Produto"):
    lucro = preco_venda - (custo_variavel + custo_fixo)
    novo_dado = pd.DataFrame([[produto, preco_venda, custo_variavel, custo_fixo, lucro]],
                              columns=["Produto", "Preço de Venda", "Custo Variável", "Custo Fixo", "Lucro"])
    df = pd.concat([df, novo_dado], ignore_index=True)
    st.experimental_rerun()

if not df.empty:
    st.subheader("Produtos Cadastrados")
    st.dataframe(df)
    
    # Gráfico de Rentabilidade
    fig = px.bar(df, x="Produto", y="Lucro", title="Rentabilidade por Produto", color="Lucro", text_auto=True)
    st.plotly_chart(fig)
    
    # Baixar CSV
    st.markdown(salvar_csv(df), unsafe_allow_html=True)
    
    # Exportar para PDF
    st.subheader("Gerar Relatório PDF")
    if st.button("📄 Exportar PDF"):
        import pdfkit
        html = df.to_html()
        pdfkit.from_string(html, "relatorio.pdf")
        with open("relatorio.pdf", "rb") as f:
            b64_pdf = base64.b64encode(f.read()).decode('utf-8')
            st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="relatorio.pdf">📥 Baixar PDF</a>', unsafe_allow_html=True)
