# =====================
# BIBLIOTECAS NECESSÁRIAS
# =====================

import pandas as pd
import numpy as np

import plotly.express as px
import inflection
import streamlit as st
from PIL import Image 


st.set_page_config( layout='wide')

# ====================================================================================
# FUNÇÕES
# ====================================================================================


# Colocando o nome dos países pelo código
countries = {
    1: "Índia",
    14: "Austrália",
    30: "Brazil", 
    37: "Canadá", 
    94: "Indonesia", 
    148: "New Zeland", 
    162: "Philippines", 
    166: "Qatar", 
    184: "Singapure", 
    189: "South Africa",
    191: "Sri Lanka", 
    208: "Turkey", 
    214: "United Arab Emirates", 
    215: "England", 
    216: "United States of America",
}

# colocando nome nas cores dos códigos
colors = {
    '3F7E00': 'darkgreen', 
    '5BA829': 'green', 
    '9ACD32': 'lightgreen', 
    'CDD614': 'orange', 
    'FFBA00': 'red', 
    'CBCBC8': 'darkred', 
    'FF7800': 'darkred',
}


# Definindo o custo do prato pelo número
def create_price_tye(price_range):
    if price_range == 1:
        return 'cheap'
    elif price_range == 2:
        return 'normal'
    elif price_range == 3:
        return 'expensive'
    elif price_range == 4:
        return 'gourmet'

# Definindo 1 como sim e 0 como não
def create_yes_no(yes_no):
    if yes_no == 1:
        return 'Yes'
    else:
        return 'No'


# Renomear as colunas do DF
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

def color_name(color_code):
    return colors[color_code]

def country_name(country_id):
    return countries[country_id]


# Aplicando as defs

def clean_code(data):
    df = data.copy()
    
    df = df.dropna()
  
    df["country"] = df.loc[:, "Country Code"].apply(lambda x: country_name(x))
    df["color_name"] = df.loc[:, "Rating color"].apply(lambda x: color_name(x))
    df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
    df["price_type"] = df.loc[:, "Price range"].apply(lambda x: create_price_tye(x))
    df["delivering_now"] = df.loc[:, "Is delivering now"].apply(lambda x: create_yes_no(x))
    df["table_booking"] = df.loc[:, "Has Table booking"].apply(lambda x: create_yes_no(x))
    df["online_delivery"] = df.loc[:, "Has Online delivery"].apply(lambda x: create_yes_no(x))
    
    return df

df = pd.read_csv('zomato.csv')
df1 = clean_code(df)


# --------------------------------------------------------
#                           Funções de gráfico
# --------------------------------------------------------


def p_mais_cidade(df1):
    pais_grf1 = df1.loc[:, ['City', 'country']].groupby('country').nunique().sort_values('City', ascending=False).reset_index()
    fig = px.bar(pais_grf1, x='country', y='City', color='country')        
    fig.update(layout_showlegend=False) 

    return fig

def p_maior_media(df1):
    pais_grf8 = df1.loc[:, ['country', 'Votes']].groupby('country').mean().sort_values('Votes', ascending=False).reset_index()       
    fig = px.bar(pais_grf8, x='Votes', y='country', color='country', orientation='h')
    fig.update(layout_showlegend=False)

    return fig


def p_culinaria(df1):
    pais_grf4 = df1.loc[:, ['Cuisines', 'country', 'Restaurant ID']].groupby('country').nunique().sort_values('Cuisines', ascending=False).reset_index()
    fig = px.treemap(pais_grf4, path=['country'], values='Cuisines', color='Cuisines' , color_continuous_scale='RdBu' )

    return fig


def p_tabela(df1):
    price = round(df1.loc[:, ['Average Cost for two', 'Currency', 'country']].groupby(['country','Currency']).mean().sort_values('Average Cost for two', ascending=False).reset_index(),2)   
    rating = round(df1.loc[:, ['Aggregate rating', 'country']].groupby('country').mean().sort_values('Aggregate rating', ascending=False).reset_index(), 2)
    df_aux = pd.merge(price, rating, how='inner')

    return df_aux

def p_mais_restaurante(df1):
    pais_grf2 = df1.loc[:, ['country', 'Restaurant ID']].groupby('country').nunique().sort_values('Restaurant ID',  ascending=False).reset_index()

    fig = px.bar(pais_grf2, x='country', y='Restaurant ID', color='country')
    fig.update(layout_showlegend=False)

    return fig

def p_rest_caros(df1):
    pais_grf3 = df1.loc[(df1['Price range'] == 4), ['country',  'Price range', 'Restaurant ID']].groupby('country').count().sort_values('Restaurant ID', ascending=False).reset_index()

    fig = px.bar(pais_grf3, x='Price range', y='country', color='country', orientation='h')
    fig.update(layout_showlegend=False)
    
    return fig


def p_entrega(df1):
    pais_grf6 = df1.loc[:, ['country', 'delivering_now']].groupby('delivering_now').count().sort_values('delivering_now', ascending=False).reset_index()
    fig = px.pie(pais_grf6, values='country', names='delivering_now')

    return fig

def p_reservas(df1):
    pais_grf7 = df1.loc[:, ['country', 'table_booking']].groupby('table_booking').count().sort_values('table_booking', ascending=False).reset_index()
    fig = px.pie(pais_grf7, values='country', names='table_booking')

    return fig

def p_online(df1):
    pais_grf6 = df1.loc[:, ['country', 'online_delivery']].groupby('online_delivery').count().sort_values('online_delivery', ascending=False).reset_index()
    fig = px.pie(pais_grf6, values='country', names='online_delivery')

    return fig

# ===================================================================
#                         Sidebar no streamlit 
# =================================================================== 

st.header('Visão Paises')


image = Image.open( 'foco.png' )
st.sidebar.image( image, width=120 )


st.sidebar.markdown('# FomeZero')
st.sidebar.markdown('## Marketplace de Restaurantes')

st.sidebar.markdown("""---""")

st.sidebar.markdown('## Filtro de Países')
country_options = st.sidebar.multiselect(
    'Selecione os países', 
    ['Philippines', 'Brazil', 'Austrália', 'United States of America',
       'Canadá', 'Singapure', 'United Arab Emirates', 'Índia',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'], 
    default=['Philippines', 'Brazil', 'Austrália', 'United States of America',
       'Canadá', 'Singapure', 'United Arab Emirates', 'Índia',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'] ) 


st.sidebar.markdown("""---""") 
st.sidebar.markdown("### Powered by Comunidade DS.")
st.sidebar.markdown("###### Talitha Oliveira")


country_sel = df1['country'].isin( country_options ) 
df1 = df1.loc[country_sel, :]


# ===================================================================
#                     Layout no streamlit 
# ===================================================================

tab1, tab2 = st.tabs( ['Visão Geral',  'Visão Restaurantes'] )


with tab1: 
    
    
    with st.container():
        st.subheader ('Paises com mais cidades registradas')
        
        fig = p_mais_cidade(df1)
        st.plotly_chart(fig, use_container_width=True)
              

        
    with st.container():
        st.subheader('Países que possuem a maior média de avaliações registrada')
        
        fig = p_maior_media(df1)         
        st.plotly_chart(fig, use_container_width=True)
        
        
        
    with st.container():
        
        col1, col2, = st.columns(2)
        
        with col1:
            
            st.subheader('Países que possuem mais culinárias distintas')   

            fig = p_culinaria(df1)
            st.plotly_chart(fig, use_container_width = True, theme='streamlit')
            
            

        with col2:
            st.subheader ('Média de custo e de avaliação dos países')

            df_aux = p_tabela(df1)
            st.dataframe(df_aux) 
        
        
        
with tab2:         

    with st.container():
        st.subheader('Países que possuem mais restaurantes registrados')

        fig = p_mais_restaurante(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    
    
    with st.container():
        st.subheader ('Paises com restaurantes mais caros')
          
        fig = p_rest_caros(df1)        
        st.plotly_chart(fig, use_container_width=True)


        
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        
        with col1:
            st.subheader('Relação de entregas ')
        
            fig = p_entrega(df1)
            st.plotly_chart(fig, use_container_width=True)


        with col2:
            st.subheader('Relação de pedidos online ')

            fig = p_online(df1)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.subheader('Relação de reservas ')

            fig = p_reservas(df1)
            st.plotly_chart(fig, use_container_width=True)
    
    
    
    

    

        
        
    
        
        

    





