import streamlit as st
import streamlit.components.v1 as components

def exibir_pagina_inicial():
    # CSS customizado
    custom_css = """
    <style>
    /* Mostra o menu lateral automaticamente em telas largas */
    @media (min-width: 768px) {
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
        }
    }

    /* Fecha o menu automaticamente após clicar no mobile */
    @media (max-width: 767px) {
        header[tabindex="0"] {
            pointer-events: none;
        }
    }
    </style>
    """
    
    meta_tags = """
    <meta property="og:title" content="Simulador de Markup e Rentabilidade - Marcos Rita + IA" />
    <meta property="og:description" content="Simule seus lucros com inteligência! Cadastre produtos, analise rentabilidade e gere relatórios com o poder da IA." />
    <meta property="og:image" content="https://simulador-markup.streamlit.app/images/banner.png" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://simulador-markup.streamlit.app" />
    """

    components.html(f"<head>{meta_tags}{custom_css}</head>", height=0)

    st.image("banner.jpg", use_container_width=True)

    st.markdown("""
    # Bem-vindo ao Simulador de Markup e Rentabilidade 🧠💰

    Com o **Simulador Marcos Rita + IA** você pode:

    ✅ Cadastrar produtos ilimitados  
    ✅ Calcular markup e margem de lucro  
    ✅ Gerar gráficos de rentabilidade  
    ✅ Inserir custos variáveis e fixos  
    ✅ Exportar relatórios em PDF  
    ✅ Salvar e carregar simulações em CSV  
    ✅ Tudo isso com um design bonito e intuitivo em azul claro e escuro!  

    🖥️ *Na versão desktop, use o menu lateral.*  
    📱 *Na versão mobile, use o menu acima (☰).*  

    **Compartilhe com seus amigos e otimize sua gestão de negócios!**
    """)
