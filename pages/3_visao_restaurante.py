from haversine import haversine 
import plotly.express as px 
import plotly.graph_objects as go 

#bibliotecas
import pandas as pd 
import streamlit as st
import numpy as np
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Restaurantes', page_icon='🍽️', layout='wide' )
#___________________________________________________________________________________
#Funções
def avg_std_time_on_traffic( df1 ):
             df_aux =(df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                         .groupby( ['City', 'Road_traffic_density'] )
                         .agg( {'Time_taken(min)' : ['mean', 'std']} ))
                     
             df_aux.columns = ['avg_time', 'std_time']
                     
             df_aux = df_aux.reset_index()
                     
             fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', 
                                       color='std_time', color_continuous_scale='RdBu',
                                       color_continuous_midpoint=np.average(df_aux['std_time']))
             return fig
                     
def avg_std_time_graph( df1 ):
             st.title("Tempo Medio de entrega por cidade")
             df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby( 'City' ).agg({'Time_taken(min)' : ['mean', 'std']})
             df_aux.columns = ['avg_time', 'std_time']
             df_aux = df_aux.reset_index()
             fig = go.Figure()
             fig.add_trace( go.Bar( name= 'Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
             fig.update_layout(barmode='group')

             return fig
    
def avg_std_time_devlivery( df1, Festival, op ):
            """
                     Esta função caucula o tempo medio e o desvio padrão do tempo de entrega.
                     Parâmetros:
                        Input:
                           - df: Dataframe com os dados necessarios para o calculo
                           - op: Tipo de operação que precisa ser calculado 
                                 'avg_time': calcula o tempo medio 
                                 'std_time' : calcula o desvio padrao do tempo 
                        Output : 
                            - df: Dataframe com 2 colunas e 1 linha.
            """
        
            df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
                         .groupby('Festival')
                         .agg({'Time_taken(min)' : ['mean', 'std']}) )
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round(df_aux.loc[df_aux['Festival'] == 'Yes', op], 2 )

            return df_aux


def distance( df1, fig ):
            if fig == False:
                 cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
                 df1['distance'] = df1.loc[:, cols].apply( lambda x:
                                                  haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                             (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1)
                 avg_distance = np.round( df1['distance'].mean() , 2)
                 return avg_distance
            else:  
                 cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
                 df1['distance'] = df1.loc[:, cols].apply( lambda x:
                                          haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                     (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1)
                 avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
                 fig = go.Figure(data = [go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
                 return fig
            
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
    
df = pd.read_csv('dataset/train.csv')

df1 = clean_code( df )

#========================================
#Barra Lateral 
#=======================================
st.header ('Marketplace - Visão Restaurante')


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
         st.title('Overal Metrics')

         col1, col2, col3, col4, col5, col6 = st.columns(6)
         with col1:
             devlivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique() )
             col1.metric('entregadores unicos', devlivery_unique)
             
         with col2:
             avg_distance = distance( df1, fig=False )
             col2.metric(' A distancia media das entregas', avg_distance)
                                                              
             
         with col3:
             df_aux = avg_std_time_devlivery( df1, 'Yes', 'avg_time' )
             col3.metric ('Tempo Médio de entrega c/ festival', df_aux)

                 
         with col4:
             df_aux = avg_std_time_devlivery( df1, 'Yes', 'std_time' )
             col4.metric ('STD de Entrega c/ Festival', df_aux)
             
             
         with col5:
             df_aux = avg_std_time_devlivery( df1, 'No', 'avg_time' )
             col5.metric ('Tempo Médio de Entrega s/ Festival', df_aux)
             
         with col6:
             df_aux = avg_std_time_devlivery( df1, 'No', 'std_time' )
             col6.metric ('STD de Entrega s/ Festival', df_aux)
              
         
     with st.container():
             st.markdown( """---""" )
             col1, col2 = st.columns( 2 )

             with col1:
                   fig = avg_std_time_graph( df1 )
                   st.plotly_chart(fig)
                 
             with col2:
                st.title('Distribuição da distancia')
                df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                             .groupby( ['City', 'Type_of_order'] )
                             .agg( {'Time_taken(min)' : ['mean', 'std']} ))
                df_aux.columns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                st.dataframe(df_aux)

    
     with st.container():
         st.markdown( """---""" )
         st.title('Distribuição do tempo')
         
         col1, col2 = st.columns(2)
         with col1:
             fig = distance( df1, fig=True )
             st.plotly_chart( fig )
             
            
         with col2:
              fig = avg_std_time_on_traffic( df1 )
              st.plotly_chart( fig )

    
     