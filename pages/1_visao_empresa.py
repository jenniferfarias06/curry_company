# Libares
from haversine import haversine 
import plotly.express as px 
import plotly.graph_objects as go 

#bibliotecas
import pandas as pd 
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa', page_icon='📉', layout='wide' )
#__________________________________________________________________________________________________
# Funções
def country_maps( df1 ):
                 
                cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
                df_aux = (df1.loc[:, cols]
                            .groupby(['City','Road_traffic_density'])
                            .median()
                            .reset_index())
        
                map = folium.Map()
            
                for index, location_info in df_aux.iterrows():
                    folium.Marker([location_info[ 'Delivery_location_latitude'],
                                   location_info['Delivery_location_longitude']],
                                   popup=location_info[['City', 'Road_traffic_density']]).add_to( map )
                    
                folium_static(map, width=1024, height=600)    
    
def Order_Share_By_Week(df1):
                   
                   df_aux1 = (df1.loc[:, ['ID', 'week_of_year'] ]
                                 .groupby('week_of_year')
                                 .count()
                                 .reset_index())
    
                   df_aux2= (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                                .groupby('week_of_year')
                                .nunique()
                                .reset_index())
        
                   df_aux = pd.merge(df_aux1, df_aux2, how='inner')
    
                   df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    
                   fg = px.line(df_aux, x = 'week_of_year', y = 'order_by_delivery')

                   return fg 
     
def order_by_week(df1):
                   
                   df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U')
                   df_aux = df1.loc[:, ['ID', 'week_of_year']]. groupby('week_of_year').count().reset_index()
                   fg = px.line(df_aux, x = 'week_of_year', y = 'ID')

                   return fg 
    
def Traffic_Order_City( df1 ):
               
                   df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                                .groupby( ['City', 'Road_traffic_density'] )
                                .count()
                                .reset_index())
    
                   fg = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size= 'ID', color = 'City')
    
                   return fg


def Traffic_Order_Share(df1):
            
               df_aux = (df1.loc[: , ['ID', 'Road_traffic_density']]
                            .groupby('Road_traffic_density')
                            .count()
                            .reset_index())

               df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', : ]
               df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

               fg = px.pie(df_aux, values = 'entregas_perc', names = 'Road_traffic_density')
     
               return fg

     
def order_metric(df1):
              #selecao de linhas
              df_aux = (df1.loc[: , ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index())
              df_aux.head()
            
              fg = px.bar(df_aux, x = 'Order_Date' , y = 'ID')

              return fg 
     
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

#_______________________________Inicio da estrutura logica do codigo _______________________________________
#__________________________________________________________________________________________________________
#Import dataset
df = pd.read_csv('dataset/train.csv')

# limpando dados 
df1 = clean_code ( df )


#========================================
#Barra Lateral 
#=======================================
st.header ('Marketplace - Visão Cliente')



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
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
  with st.container():
      fg = order_metric(df1)
      st.markdown(' # Orders by Day')
      st.plotly_chart(fg, use_container_width=True)
      

  with st.container():
      col1, col2 = st.columns(2)
      
      with col1:
          st.header('Traffic Order Share')
          fg = Traffic_Order_Share(df1)
          st.plotly_chart(fg, use_container_width=True)
          
    
      with col2:
           st.header('Traffic Order City')
           fg = Traffic_Order_City( df1 )
           st.plotly_chart(fg, use_container_width=True)

          
with tab2:
    with st.container():
         st.markdown(' # Order by Week ')
         fg = order_by_week(df1)
         st.plotly_chart(fg, use_container_width=True)
               
      
    with st.container():
        st.markdown('# Order Share By Week')
        fg = Order_Share_By_Week(df1)
        st.plotly_chart(fg, use_container_width=True)
      
      
with tab3:
        st.markdown('# Country Maps')
        country_maps( df1 )                                                      
