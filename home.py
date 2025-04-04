import streamlit as st
import streamlit.components.v1 as components

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
        <style>
            .fade-in {
                animation: fadeIn 2s ease-in forwards;
                opacity: 0;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .content-box {
                background: #1f2c3a;
                padding: 20px;
                border-radius: 15px;
                color: white;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                margin-top: 20px;
            }
        </style>
        <div class="fade-in">
            <div class="content-box">
                <h1>Bem-vindo ao Simulador de Markup e Rentabilidade 🧠💰</h1>
                <p>Com o <strong>Simulador Marcos Rita + IA</strong> você pode:</p>
                <ul>
                    <li>✅ Cadastrar produtos ilimitados</li>
                    <li>✅ Calcular markup e margem de lucro</li>
                    <li>✅ Gerar gráficos de rentabilidade</li>
                    <li>✅ Inserir custos variáveis e fixos</li>
                    <li>✅ Exportar relatórios em PDF</li>
                    <li>✅ Salvar e carregar simulações em CSV</li>
                    <li>✅ Tudo isso com um design bonito e intuitivo em azul claro e escuro!</li>
                </ul>
                <p>👉 Use o menu lateral para acessar as funcionalidades.</p>
                <p><strong>Compartilhe com seus amigos e otimize sua gestão de negócios!</strong></p>
            </div>
        </div>
    """, unsafe_allow_html=True)
