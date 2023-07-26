# =====================
# BIBLIOTECAS NECESSÁRIAS
# =====================

import pandas as pd
import numpy as np

import plotly.express as px
import inflection
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import streamlit as st
from PIL import Image 


st.set_page_config(  layout='wide')

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


# Definindo 1 como sim e 0 como não
def create_price_tye(price_range):
    if price_range == 1:
        return 'cheap'
    elif price_range == 2:
        return 'normal'
    elif price_range == 3:
        return 'expensive'
    elif price_range == 4:
        return 'gourmet'

# Definindo o custo do prato pelo número
def create_yes_no(yes_no):
    if yes_no == 1:
        return 'Yes'
    else:
        return 'No'


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
    
    return df

def color_name(color_code):
    return colors[color_code]

def country_name(country_id):
    return countries[country_id]


# Aplicando as defs

def clean_code(data):
    df = data.copy()
    
    df = df.dropna()
  
    # Utilizando .loc para atribuir os valores diretamente no DataFrame original
    df.loc[:, "country"] = df.loc[:, "Country Code"].apply(lambda x: country_name(x))
    df.loc[:, "color_name"] = df.loc[:, "Rating color"].apply(lambda x: color_name(x))
    df.loc[:, "Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
    df.loc[:, "price_type"] = df.loc[:, "Price range"].apply(lambda x: create_price_tye(x))
    df.loc[:, "delivering_now"] = df.loc[:, "Is delivering now"].apply(lambda x: create_yes_no(x))
    df.loc[:, "table_booking"] = df.loc[:, "Has Table booking"].apply(lambda x: create_yes_no(x))
    df.loc[:, "online_delivery"] = df.loc[:, "Has Online delivery"].apply(lambda x: create_yes_no(x))
    
    return df

df = pd.read_csv('zomato.csv')
df1 = clean_code(df)


# --------------------------------------------------------
#                    Funções de gráfico
# --------------------------------------------------------

def c_avaliacao(df1):
    cid_grf1 = round(df1.loc[:, ['City', 'Aggregate rating', 'country']].groupby('City').mean(numeric_only=True).sort_values('Aggregate rating', ascending=False).reset_index(), 1)
    fig = px.funnel(cid_grf1.head(10), y='City', x='Aggregate rating', color='City')
    fig.update(layout_showlegend=False)

    return fig


def c_culinaria(df1):
    cid_grf5 = df1.loc[:, ['City', 'Cuisines', 'country']].groupby(['City','country']).nunique().sort_values('Cuisines', ascending= False).reset_index()
    fig= px.bar(cid_grf5.head(10), x='City', y='Cuisines', color='country')

    return fig


def c_mais_menos(df1, preco, asc):


    """
    preco = 1: Price range
    preco = 2: Average Cost for two

    """
    if preco == 1: 
        grf1 = round(df1.loc[:, ['City', 'Price range', 'country' ]].groupby(['City', 'country' ]).mean().sort_values('Price range', ascending=asc).reset_index(), 2)
        fig = px.bar(grf1.head(5), x='Price range', y='City', color='country')

    else:
        grf2 = round(df1.loc[:, ['City', 'Average Cost for two', 'country']].groupby(['City', 'country']).mean().sort_values('Average Cost for two', ascending=asc).reset_index(), 2)
        fig = px.bar(grf2.head(5), x='Average Cost for two', y='City', color='country')


    return fig

        
def c_restaurante(df1):
    cid_grf1 = df1.loc[:, ['City', 'Restaurant ID', 'country']].groupby('City').count().sort_values('Restaurant ID', ascending=False).reset_index()
    fig = px.bar(cid_grf1.head(7), x='City', y='Restaurant ID', color='City')
    fig.update(layout_showlegend=False)

    return fig


def c_rest_nota(df1, valor):

    """valor = 4 (nota maior a 4)
        valor = 2 (nota menor que 2) """

    if valor == 4:
        cid_grf2 = df1.loc[(df1['Aggregate rating'] >= 4),['City', 'Restaurant ID', 'country'] ].groupby(['City', 'country']).count().sort_values('Restaurant ID', ascending=False).reset_index()
        fig= px.bar(cid_grf2.head(5), x='City', y='Restaurant ID', color='country')

    else:
        cid_grf3 = df1.loc[(df1['Aggregate rating'] <= 2),['City', 'Restaurant ID', 'country'] ].groupby(['City', 'country']).count().sort_values('Restaurant ID', ascending=False).reset_index()
        fig = px.bar(cid_grf3.head(5), x='City', y='Restaurant ID', color='country')

    return fig
# ===================================================================
#                   Slidebar no streamlit 
# =================================================================== 

st.header('Visão Cidades')


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
#                      Layout no streamlit  
# ===================================================================

tab1, tab2= st.tabs( ['Visão Geral', 'Visão Restaurantes'] )


with tab1: 
    
    
    with st.container():
        st.subheader ('Cidade melhores avaliadas')

        fig= c_avaliacao(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    
    with st.container():
        st.subheader ('Top 5 cidades com mais tipos de culinária distintas')
    
        fig=c_culinaria(df1)
        st.plotly_chart(fig, use_container_width=True)
        

        
    with st.container():
        col1, col2 = st.columns(2)
        
        
        with col1:
            
            st.subheader ('Top 5 cidades cidades mais caras em geral')
            
            fig = c_mais_menos(df1, 1, False)
            st.plotly_chart(fig, use_container_width=True)
            
            
        with col2:
            st.subheader ('Top 5 cidade mais baratas em geral')

            fig = c_mais_menos(df1, 1, True)
            st.plotly_chart(fig, use_container_width=True)
            
            
    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader ('Top 5 cidades mais caras para 2 pessoas')
        
        
            fig = c_mais_menos(df1, 2, False)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader ('Top 5 cidades mais baratas para 2 pessoas')
                    
            fig = c_mais_menos(df1, 2, True)
            st.plotly_chart(fig, use_container_width=True)
        
        

with tab2: 
    
    
    with st.container():
        st.subheader ('Top 5 cidades com mais restaurantes registrados')

        fig = c_restaurante(df1)        
        st.plotly_chart(fig, use_container_width=True)
        
        
    
    with st.container():
        col1, col2 = st.columns( 2 )
        
        
        with col1: 

            st.subheader('Top 10 cidades com restaurantes com nota média acima de 4')

            
            fig = c_rest_nota(df1, 4)            
            st.plotly_chart(fig, use_container_width=True)
    
    
        with col2:
            st.subheader('Top 5 cidades com restaurantes com nota média abaixo de 2.5')   

            fig = c_rest_nota(df1, 2)
            st.plotly_chart(fig, use_container_width=True)
        
    




        

        
        
        
        


    
    
    
    



            
        
        
    
        
        

    





