import streamlit as st
import home
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import os
import base64

st.set_page_config(page_title="Simulador de Markup - Marcos Rita + IA", layout="wide")

# CSS personalizado com dark mode e menus adaptativos
st.markdown("""
    <style>
    body {
        background-color: #0b1d36;
        color: white;
    }
    .menu-lateral button, .menu-container button {
        background-color: #0f4c75;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s;
    }
    .menu-lateral button:hover, .menu-container button:hover {
        background-color: #3282b8;
    }
    @media (min-width: 768px) {
        .menu-horizontal { display: none !important; }
    }
    @media (max-width: 767px) {
        .menu-lateral { display: none !important; }
    }
    .menu-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Simulador de Markup e Rentabilidade")

# Inicialização do estado da sessão
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = "Início"
if 'produtos' not in st.session_state:
    st.session_state['produtos'] = []
if 'custos_variaveis' not in st.session_state:
    st.session_state['custos_variaveis'] = []
if 'custos_fixos' not in st.session_state:
    st.session_state['custos_fixos'] = []

def selecionar_pagina(p):
    st.session_state['pagina'] = p

opcoes_menu = [
    "Início", "Produtos", "Custos Variáveis", "Custos Fixos",
    "Simulador", "Gráfico de Rentabilidade", "Relatório/Gráfico", "Salvar/Carregar"
]

# Menu lateral (desktop)
st.markdown("<div class='menu-lateral'>", unsafe_allow_html=True)
with st.sidebar:
    for i, nome in enumerate(opcoes_menu):
        if st.button(nome, key=f"menu_lateral_{i}"):
            selecionar_pagina(nome)
st.markdown("</div>", unsafe_allow_html=True)

# Menu topo (mobile)
st.markdown("<div class='menu-horizontal'><div class='menu-container'>", unsafe_allow_html=True)
for i, nome in enumerate(opcoes_menu):
    if st.button(nome, key=f"menu_topo_{i}"):
        selecionar_pagina(nome)
st.markdown("</div></div>", unsafe_allow_html=True)

# Navegação de páginas
pagina = st.session_state['pagina']

if pagina == "Início":
    home.exibir_pagina_inicial()

elif pagina == "Simulador":
    st.subheader("Simulador de Markup e Rentabilidade")
    if not st.session_state['produtos'] or not st.session_state['custos_variaveis'] or not st.session_state['custos_fixos']:
        st.info("\U0001F4CC Cadastre os produtos, custos variáveis e custos fixos para simular o markup e a rentabilidade.")
    else:
        st.success("Tudo pronto para simular! Explore os gráficos no menu acima ou lateral.")

elif pagina == "Gráfico de Rentabilidade":
    st.subheader("Gráfico de Rentabilidade")
    if not st.session_state['produtos']:
        st.info("\U0001F4CC Cadastre produtos, custos variáveis e fixos antes de gerar os gráficos.")
    else:
        st.success("Pronto para visualizar seus dados!")

elif pagina == "Produtos":
    st.subheader("Cadastro de Produtos")
    with st.form("form_produto"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço de Venda (R$)", min_value=0.0)
        custo = st.number_input("Custo (R$)", min_value=0.0)
        submit = st.form_submit_button("Adicionar Produto")
        if submit:
            lucro = preco - custo
            markup = preco / custo if custo else 0
            st.session_state['produtos'].append({"Produto": nome, "Preco Venda": preco, "Custo": custo, "Lucro": lucro, "Markup": markup})
            st.success("Produto adicionado!")

    if st.session_state['produtos']:
        df_produtos = pd.DataFrame(st.session_state['produtos'])
        st.dataframe(df_produtos)

elif pagina == "Custos Variáveis":
    st.subheader("Custos Variáveis")
    with st.form("form_cv"):
        nome = st.text_input("Nome do Custo Variável")
        valor = st.number_input("Valor (R$)", min_value=0.0)
        add = st.form_submit_button("Adicionar")
        if add:
            st.session_state['custos_variaveis'].append({"Nome": nome, "Valor": valor})
            st.success("Custo Variável adicionado!")

    if st.session_state['custos_variaveis']:
        df_cv = pd.DataFrame(st.session_state['custos_variaveis'])
        st.dataframe(df_cv)

elif pagina == "Custos Fixos":
    st.subheader("Custos Fixos")
    with st.form("form_cf"):
        nome = st.text_input("Nome do Custo Fixo")
        valor = st.number_input("Valor (R$)", min_value=0.0)
        add = st.form_submit_button("Adicionar")
        if add:
            st.session_state['custos_fixos'].append({"Nome": nome, "Valor": valor})
            st.success("Custo Fixo adicionado!")

    if st.session_state['custos_fixos']:
        df_cf = pd.DataFrame(st.session_state['custos_fixos'])
        st.dataframe(df_cf)

elif pagina == "Relatório/Gráfico":
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

        if st.button("\U0001F4C4 Gerar PDF"):
            caminho_pdf = gerar_pdf(df_produtos, df_cv, df_cf, lucro_total, markup_medio)
            with open(caminho_pdf, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_simulador.pdf">\U0001F4C5 Baixar PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

elif pagina == "Salvar/Carregar":
    st.subheader("Salvar e Carregar Dados")

    if st.button("Salvar Dados como CSV"):
        df_produtos = pd.DataFrame(st.session_state['produtos'])
        df_produtos.to_csv("dados_produtos.csv", index=False)
        st.success("Arquivo CSV salvo como dados_produtos.csv")

    arquivo = st.file_uploader("Carregar Arquivo CSV", type="csv")
    if arquivo is not None:
        df_carregado = pd.read_csv(arquivo)
        st.session_state['produtos'] = df_carregado.to_dict(orient='records')
        st.success("Arquivo carregado com sucesso!")

def gerar_pdf(df_produtos, df_cv, df_cf, lucro_total, markup_medio):
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

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Resumo Financeiro", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 8, f"Lucro Total Estimado: R${lucro_total:.2f}", ln=True)
    pdf.cell(200, 8, f"Markup Médio: {markup_medio:.2f}x", ln=True)

    caminho = os.path.join(os.getcwd(), "relatorio_simulador.pdf")
    pdf.output(caminho)
    return caminho
