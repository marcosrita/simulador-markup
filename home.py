import streamlit as st
import streamlit.components.v1 as components

# Estilo customizado para menus responsivos
st.markdown("""
    <style>
        @media (max-width: 768px) {
            .mobile-hint {
                display: block;
            }
            .desktop-hint {
                display: none;
            }
        }
        @media (min-width: 769px) {
            .mobile-hint {
                display: none;
            }
            .desktop-hint {
                display: block;
            }
        }
    </style>
""", unsafe_allow_html=True)

def exibir_pagina_inicial():
    # Meta tags para compartilhamento (HTML customizado)
    meta_tags = """
    <meta property="og:title" content="Simulador de Markup e Rentabilidade - Marcos Rita + IA" />
    <meta property="og:description" content="Simule seus lucros com inteligência! Cadastre produtos, analise rentabilidade e gere relatórios com o poder da IA." />
    <meta property="og:image" content="https://simulador-markup.streamlit.app/A_digital_graphic_design_image_represents_a_Brazil.png" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://simulador-markup.streamlit.app" />
    """
    components.html(f"<head>{meta_tags}</head>", height=0)

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

    <p class="desktop-hint">👉 Use o <strong>menu lateral</strong> para acessar as funcionalidades.</p>
    <p class="mobile-hint">👉 Use o <strong>menu acima</strong> para acessar as funcionalidades.</p>

    **Compartilhe com seus amigos e otimize sua gestão de negócios!**
    """, unsafe_allow_html=True)
