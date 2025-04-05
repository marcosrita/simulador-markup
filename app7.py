import streamlit as st
import home
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Simulador de Markup - Marcos Rita + IA", layout="wide")

# Estilo global azul royal
st.markdown("""
    <style>
        body {
            background-color: #e6f0fa;
        }
        .css-18e3th9 {
            background-color: #0f4c75;
        }
        .stButton>button {
            background-color: #0f4c75;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
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

# Estado inicial
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = "Início"
if 'produtos' not in st.session_state:
    st.session_state['produtos'] = []
if 'custos_variaveis' not in st.session_state:
    st.session_state['custos_variaveis'] = []
if 'custos_fixos' not in st.session_state:
    st.session_state['custos_fixos'] = []

# Função para navegar
def selecionar_pagina(p):
    st.session_state['pagina'] = p

# Menu lateral (desktop)
with st.sidebar:
    st.markdown("<div class='menu-lateral'>", unsafe_allow_html=True)
    for nome in ["Início", "Produtos", "Custos Variáveis", "Custos Fixos", "Simulador", "Gráfico", "Relatório/Gráfico", "Salvar/Carregar"]:
        if st.button(nome, key=f"menu_lateral_{nome}"):
            selecionar_pagina(nome)
    st.markdown("</div>", unsafe_allow_html=True)

# Menu horizontal (mobile)
st.markdown("<div class='menu-horizontal'><div class='menu-container'>", unsafe_allow_html=True)
for nome in ["Início", "Produtos", "Custos Variáveis", "Custos Fixos", "Simulador", "Gráfico", "Relatório/Gráfico", "Salvar/Carregar"]:
    if st.button(nome, key=f"menu_topo_{nome}"):
        selecionar_pagina(nome)
st.markdown("</div></div>", unsafe_allow_html=True)

# Roteamento
pagina = st.session_state['pagina']

import streamlit as st
import home
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Simulador de Markup - Marcos Rita + IA", layout="wide")

# Estilo global azul royal
st.markdown("""
    <style>
        body {
            background-color: #e6f0fa;
        }
        .css-18e3th9 {
            background-color: #0f4c75;
        }
        .stButton>button {
            background-color: #0f4c75;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
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

# Estado inicial
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

# Menu lateral (desktop)
with st.sidebar:
    st.markdown("<div class='menu-lateral'>", unsafe_allow_html=True)
    for nome in ["Início", "Produtos", "Custos Variáveis", "Custos Fixos", "Simulador", "Gráfico", "Relatório/Gráfico", "Salvar/Carregar"]:
        if st.button(nome, key=f"menu_lateral_{nome}"):
            selecionar_pagina(nome)
    st.markdown("</div>", unsafe_allow_html=True)

# Menu horizontal (mobile)
st.markdown("<div class='menu-horizontal'><div class='menu-container'>", unsafe_allow_html=True)
for nome in ["Início", "Produtos", "Custos Variáveis", "Custos Fixos", "Simulador", "Gráfico", "Relatório/Gráfico", "Salvar/Carregar"]:
    if st.button(nome, key=f"menu_topo_{nome}"):
        selecionar_pagina(nome)
st.markdown("</div></div>", unsafe_allow_html=True)

pagina = st.session_state['pagina']

if pagina == "Início":
    home.exibir_pagina_inicial()

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

elif pagina == "Simulador":
    st.subheader("Simulador de Markup e Rentabilidade")
    if not st.session_state['produtos']:
        st.warning("Adicione produtos para simular.")
    else:
        df = pd.DataFrame(st.session_state['produtos'])
        st.write("Resumo:")
        st.dataframe(df)
        st.success("Pronto para simular!")

elif pagina == "Gráfico":
    if st.session_state['produtos']:
        df = pd.DataFrame(st.session_state['produtos'])
        st.subheader("Gráfico de Lucro")
        st.plotly_chart(px.bar(df, x="Produto", y="Lucro", text_auto=True))

        st.subheader("Gráfico de Markup")
        st.plotly_chart(px.bar(df, x="Produto", y="Markup", text_auto=True))
    else:
        st.info("Adicione produtos para visualizar os gráficos.")

elif pagina == "Relatório/Gráfico":
    if st.session_state['produtos']:
        df_prod = pd.DataFrame(st.session_state['produtos'])
        df_cv = pd.DataFrame(st.session_state['custos_variaveis']) if st.session_state['custos_variaveis'] else pd.DataFrame(columns=["Nome", "Valor"])
        df_cf = pd.DataFrame(st.session_state['custos_fixos']) if st.session_state['custos_fixos'] else pd.DataFrame(columns=["Nome", "Valor"])
        lucro_total = df_prod['Lucro'].sum()
        markup_medio = df_prod['Markup'].mean()

        if st.button("📄 Gerar PDF"):
            caminho = gerar_pdf(df_prod, df_cv, df_cf, lucro_total, markup_medio)
            with open(caminho, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="relatorio_simulador.pdf">📥 Baixar PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Adicione produtos para gerar relatório.")

elif pagina == "Salvar/Carregar":
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
    for _, row in df_produtos.iterrows():
        pdf.cell(200, 8, f"{row['Produto']}: Venda=R${row['Preco Venda']:.2f} | Custo=R${row['Custo']:.2f} | Lucro=R${row['Lucro']:.2f} | Markup={row['Markup']:.2f}x", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Custos Variáveis", ln=True)
    pdf.set_font("Arial", size=10)
    for _, row in df_cv.iterrows():
        pdf.cell(200, 8, f"{row['Nome']}: R${row['Valor']:.2f}", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Custos Fixos", ln=True)
    pdf.set_font("Arial", size=10)
    for _, row in df_cf.iterrows():
        pdf.cell(200, 8, f"{row['Nome']}: R${row['Valor']:.2f}", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Resumo Financeiro", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 8, f"Lucro Total Estimado: R${lucro_total:.2f}", ln=True)
    pdf.cell(200, 8, f"Markup Médio: {markup_medio:.2f}x", ln=True)

    caminho = os.path.join(os.getcwd(), "relatorio_simulador.pdf")
    pdf.output(caminho)
    return caminho

