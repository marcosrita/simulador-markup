import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Simulador de Markup e Rentabilidade - Marcos Rita + IA",
    page_icon="📊",
    layout="wide"
)

# Meta tags para compartilhamento (HTML customizado)
meta_tags = """
<meta property="og:title" content="Simulador de Markup e Rentabilidade - Marcos Rita + IA" />
<meta property="og:description" content="Simule seus lucros com inteligência! Cadastre produtos, analise rentabilidade e gere relatórios com o poder da IA." />
<meta property="og:image" content="https://simulador-markup.streamlit.app/A_digital_graphic_design_image_represents_a_Brazil.png" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://simulador-markup.streamlit.app" />
"""

components.html(f"""
    <head>{meta_tags}</head>
""", height=0)

# Página de apresentação
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

👉 Use o menu lateral para acessar as funcionalidades.

**Compartilhe com seus amigos e otimize sua gestão de negócios!**
""")
