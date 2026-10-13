import streamlit as st 
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon="🎲",
    layout='wide' 
)



image = Image.open( 'image.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown('# Cury Campany')
st.sidebar.markdown('## Fastest delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Cury Company Growth Dashboard')

st.markdown(
    """
    Growth Dashboard foi construido para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como ultilizar esse Growth Dashboard ?
    - Vião Empresa:
         - Visãp Gerencial: Métricas gerais de comportamento.
         - Visão tática : Indicadores semanais de crescimeto.
         - Visão geográfica: Insights de geolocalização.
    - Visão Entregador:
         - Acompanhamento dos indicadores semanais de crescimento.
    -Visão Restaurante:
         - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for Help
    - Time de Data Science no Discord 
      - @meigarom
    """)