# home.py

import streamlit as st

def exibir_pagina_inicial():
    st.markdown("""
        <style>
        .titulo-bemvindo {
            text-align: center;
            color: #0f4c75;
            font-size: 2.5rem;
            margin-top: 1rem;
        }
        .mensagem-bemvindo {
            text-align: center;
            color: #3282b8;
            font-size: 1.2rem;
            margin-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.image("banner.jpg", use_container_width=True)

    st.markdown('<div class="titulo-bemvindo">Bem-vindo ao Simulador de Markup e Rentabilidade!</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="mensagem-bemvindo">
            📊 Com este simulador, você poderá cadastrar seus produtos, calcular o markup ideal, visualizar a rentabilidade, 
            gerar relatórios em PDF e muito mais.<br><br>
            👇 Use o menu lateral (no desktop) ou o menu superior (no mobile) para começar.
        </div>
    """, unsafe_allow_html=True)
