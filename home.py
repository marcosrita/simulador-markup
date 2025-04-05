import streamlit as st

def exibir_pagina_inicial():
    st.image("banner.jpg", use_column_width=True)
    st.markdown(
        """
        <h2 style='text-align: center; color: #0f4c75;'>Bem-vindo ao Simulador de Markup e Rentabilidade!</h2>
        <p style='text-align: center; font-size: 18px; color: #3282b8;'>
            Desenvolvido por Marcos Rita + IA para te ajudar a tomar decisões financeiras com clareza e estratégia.
        </p>
        """,
        unsafe_allow_html=True
    )
