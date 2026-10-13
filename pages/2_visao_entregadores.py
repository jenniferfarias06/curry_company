from haversine import haversine 
import plotly.express as px 
import plotly.graph_objects as go 

#bibliotecas
import pandas as pd 
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Entregadores', page_icon='🚚', layout='wide' )
#__________________________________________________________________________________________________
# Funções
def top_delivers(df1, top_asc=False):
            df2_max =(df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)', 'City']]
                         .groupby(['City', 'Delivery_person_ID'])
                         .mean()
                         .sort_values(['City','Time_taken(min)'], ascending = top_asc).reset_index())
                    
            df_aux01 = df2_max.loc[df2_max['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2_max.loc[df2_max['City'] == 'Urban', :].head(10)
            df_aux03 = df2_max.loc[df2_max['City'] == 'Semi-Urban', :].head(10)
            df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)

            return df3 

     
def clean_code(df1):
        """ Eta função tem a responsabilidade de limpar o dataframe 
        
            Tipos de limpeza:
            1. Remoção dos dados NaN
            2. Mudança do tipo da coluna de dados 
            3. Remoção dos espaços das variaveis de texto
            4. Formatação da coluna de datas
            5. Limpeza da coluna de tempo (remoção do texto da variavel numerica)


            Input : Dataframe 
            Output : Dataframe
        """
        #Limpeza
        linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
        df1 = df1.loc[linhas_selecionadas, :].copy()
        
        linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
        df1 = df1.loc[linhas_selecionadas, :].copy()
        
        linhas_selecionadas = (df1['City'] != 'NaN ')
        df1 = df1.loc[linhas_selecionadas, :].copy()
        
        linhas_selecionadas = (df1['Festival'] != 'NaN ')
        df1 = df1.loc[linhas_selecionadas, :].copy()
        
        
        df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
        
        df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
        
        df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')
        
        
        linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
        df1 = df1.loc[linhas_selecionadas, :].copy()
        df1 ['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
        
        
        df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
        df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
        df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
        df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
        df1.loc[:,  'City'] = df1.loc[:, 'City'].str.strip()
        df1.loc[:,  'Festival'] = df1.loc[:, 'Festival'].str.strip()
           
        df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split(' ')[1])
        
        df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

        return df1 
    
# import dataset
df = pd.read_csv('dataset/train.csv')

df1 = clean_code( df )

#========================================
#Barra Lateral 
#=======================================
st.header ('Marketplace - Visão Entregadores')

image = Image.open( 'image.png' )
st.sidebar.image( image, width=120 )


st.sidebar.markdown('# Cury Campany')
st.sidebar.markdown('## Fastest delivery in Town')
st.sidebar.markdown("""---""")


st.sidebar.markdown ('## selecione uma data limite')
from datetime import datetime
data_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 6, 6),
    format='DD-MM-YYYY'
)

st.sidebar.markdown("""---""")


trafffic_options = st.sidebar.multiselect(
    'Quais as condiçoes do trânsito', 
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

#filtro de data
linhas_selecionadas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas_selecionadas, :]


#filtro de traffic
linhas_selecionadas = df1['Road_traffic_density'].isin( trafffic_options )
df1 = df1.loc[linhas_selecionadas, :]



#========================================
#Layout no streamlit
#=======================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '-', '-'])

with tab1:
     with st.container():
         st.title('Overall Metrics')
    
         col1, col2, col3, col4 = st.columns(4, gap='Medium')
         with col1:
               # A maior idade dos entregadores
               maior_idade = df1.loc[:, "Delivery_person_Age"].max()
               col1.metric('Maior idade', maior_idade)

         with col2:
               # A menor idade dos entregadores
               menor_idade = df1.loc[:, "Delivery_person_Age"].min()
               col2.metric('Menor idade', menor_idade)
             
         with col3:
               # A melhor condição de veiculo 
               melhor_condicao = df1.loc[:, "Vehicle_condition"].max()
               col3.metric('Melhor condição', melhor_condicao)
              
         with col4:
               # A pior condição de veiculo
               pior_condicao = df1.loc[:, "Vehicle_condition"].min()
               col4.metric('Pior condição', pior_condicao)
              

     with st.container():
         st.markdown("""---""")
         st.title('Avaliacoes')

         col1, col2 = st.columns(2)
         with col1:
             st.markdown( '##### avaliacao media por entregador')
             df_Ratings = (df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                 .groupby('Delivery_person_ID')
                 .mean()
                 .reset_index())
             st.dataframe(df_Ratings)
             
         with col2:
             st.markdown( '##### Avaliacao media por transito')
             df_Ratings3 = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                               .groupby('Road_traffic_density')
                               .agg({'Delivery_person_Ratings': ['mean', 'std']}))

             df_Ratings3.columns =  ['mean_Ratings', 'std_Ratings']
             df_Ratings3 = df_Ratings3.reset_index()
             st.dataframe(df_Ratings3)


             st.markdown( '##### avaliacao media por clima')  
             df_Ratings2 = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                               .groupby('Weatherconditions')
                               .agg({'Delivery_person_Ratings': ['mean', 'std']}))

             df_Ratings2.columns =  ['mean_Ratings', 'std_Ratings']
             df_Ratings2 = df_Ratings2.reset_index()
             st.dataframe(df_Ratings2)
             
     with st.container(): 
          st.markdown("""---""")
          st.title('Velocidade de entrega')
         
          col1, col2 = st.columns(2)
          with col1:
              st.subheader( 'Top entregadores mais rapidos')
              df3 = top_delivers(df1, top_asc=True)
              st.dataframe(df3)


          with col2:
              st.subheader('Top entregadores mais lentos')
              df3 = top_delivers(df1, top_asc=False)
              st.dataframe(df3)
              
                    