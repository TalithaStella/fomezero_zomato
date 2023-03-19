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
#                         FUNÇÕES
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
#                    Funções de gráfico
# --------------------------------------------------------

def diverdidade(df1):
    pais_grf4 = df1.loc[:, ['Cuisines', 'country', 'Restaurant ID']].groupby('country').nunique().sort_values('Cuisines', ascending=False).reset_index()

    fig= px.bar(pais_grf4.head(10), x='country', y='Cuisines')
    
    #Creating the text variable
    text = " ".join(cat for cat in df1.Cuisines)

    # Generate word cloud
    word_cloud = WordCloud(
        width=650,
        height=200,
        random_state=1,

        collocations=False,
        stopwords=STOPWORDS,
    ).generate(text)

    plt.imshow(word_cloud)
    plt.axis("off")
    fig = plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    return fig


def melhor_pior(df1, asc):
    
    cuis_grf2 = round(df1.loc[:, ['Cuisines', 'Aggregate rating']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=asc).reset_index().iloc[:10, :], 2)
    fig = px.bar(cuis_grf2, x='Cuisines', y='Aggregate rating', color='Cuisines')
    fig.update(layout_showlegend=False)
    
    return fig


def caro_barato(df1, preco):

    """ preco = caro: pratos 'Expensive' ou 'Gourmet' e média avaliação < 2.5
                Barato: pratos 'Normal' ou 'Cheap' e média avaliação > 4.5 """

    if preco == 'caro':

        condicao = (df1['Price range'] >= 3) & (df1['Aggregate rating'] <= 2.5)
        grf_data = round(df1.loc[ condicao, ['Cuisines', 'Aggregate rating']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=True).reset_index().iloc[:10, :], 2)

    else:
        condicao = (df1['Price range'] <= 2) & (df1['Aggregate rating'] >= 4.5)
        grf_data = round(df1.loc[ condicao, ['Cuisines', 'Aggregate rating']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=True).reset_index().iloc[:10, :], 2)

    return grf_data



def brasil(df1, asc):

    br = df1.loc[(df1['Cuisines'] == 'Brazilian'),['Restaurant Name', 'Aggregate rating'] ].groupby('Restaurant Name').mean().sort_values('Aggregate rating', ascending=asc).reset_index().iloc[1, 0]

    return br



def rest_col(df1, col):

    if col == 'indian':
        culinaria = df1.loc[(df1['Cuisines'] == 'North Indian'),['Restaurant Name', 'Aggregate rating'] ].groupby('Restaurant Name').mean().sort_values('Aggregate rating', ascending=False).reset_index().iloc[1, 0]
    else:
        culinaria = df1.loc[(df1['Cuisines'] == 'Mineira'),['Restaurant Name', 'Aggregate rating'] ].groupby('Restaurant Name').mean().sort_values('Aggregate rating', ascending=True).reset_index().iloc[0, 0]
    return culinaria



def votos(df1, asc):
    fig = df1.loc[:, ['Restaurant Name', 'Votes']].groupby('Restaurant Name').sum().sort_values('Votes', ascending=asc).reset_index().iloc[:10, :]
    return fig



def nota(df1, asc):

    grf = df1.loc[:, ['Restaurant Name', 'Aggregate rating']].groupby('Restaurant Name').mean().sort_values('Aggregate rating', ascending=asc).reset_index().iloc[:10, :2]
    return grf


def preco(df1, asc):

    grf = df1.loc[:, ['Restaurant Name', 'price_type', 'Price range']].groupby('Restaurant Name').max().sort_values('Price range', ascending=asc).reset_index().iloc[:10, :2]
    return grf

# ===================================================================
#                    Slidebar no streamlit  
# =================================================================== 

st.header('Visão culinárias')


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
#                         Layout no streamlit  
# ===================================================================

tab1, tab2 = st.tabs( ['Visão Culinárias',  'Visão Restaurantes'] )

with tab1:
    
    with st.container():
        st.sidebar.markdown("""---""") 
        st.subheader ('Diversidade culinária')


        fig = diverdidade(df1)
        st.pyplot(fig)


    with st.container():
        st.markdown("""---""") 
        col1, col2  = st.columns(2)

        with col1:

            st.subheader ('Top 10 melhores cozinhas')


            fig = melhor_pior(df1, False)
            st.plotly_chart(fig, use_container_width=True)



        with col2:
            st.subheader ('Top 10 piores cozinhas ')

            fig = melhor_pior(df1, True)
            st.plotly_chart(fig, use_container_width=True)




    with st.container():

        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Top 10 culinárias mais caras e pior avaliada')
            st.markdown("###### Para pratos 'Expensive' ou 'Gourmet' e média avaliação < 2.5")      


            grf_data = caro_barato(df1, 'caro')
            st.dataframe(grf_data)

        with col2:
            st.subheader('Top 10 culinárias mais baratas e melhor avaliada')
            st.markdown("###### Para pratos 'Normal' ou 'Cheap' e média avaliação > 4.5")


            grf_data = caro_barato(df1, 'barato')
            st.dataframe(grf_data)
            
            
            
with tab2:


    col1, col2 = st.columns(2)

    with col1:
        st.markdown ('##### Melhor restaurante Brasileiro ')
        
        br = brasil(df1, False)
        col1.metric( '', br )


    with col2:
        st.markdown ('##### Pior restaurante Brasileiro ')
        br = brasil(df1, True)
        col2.metric( '', br )

    st.markdown("""---""")

    
    col1, col2 = st.columns(2)    


    with col1:
        st.markdown ('##### Restaurante da melhor culinária (north Indian)')
      
        culinaria = rest_col(df1, 'indian')
        col1.metric( '', culinaria)
        
        

    with col2:
        st.markdown ('##### Restaurante da pior culinária (Mineira) ')
        
        culinaria = rest_col(df1, 'mineira')
        col2.metric( '', culinaria)
        
        
    st.markdown("""---""")
        
        
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Restaurantes com mais votos realizados')
        
        fig = votos(df1, False)
        fig = px.bar(fig, x='Restaurant Name', y='Votes')
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader('Restaurantes com menos votos realizados')

        fig = votos(df1, True)
        st.dataframe(fig)
        

    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Restaurantes com maior nota média')
        
            grf = nota(df1, False)
            st.dataframe(grf)
            
            
        with col2:
            st.subheader('Restaurantes com menor nota média')            
            
            grf = nota(df1, True)
            st.dataframe(grf)
            
            
    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Restaurantes mais caros')
            
            
            grf = preco(df1, False)
            st.dataframe(grf)
            
        with col2:
            st.subheader('Restaurantes mais baratos')            
            
            grf = preco(df1, True)
            st.dataframe(grf)
            
            
   




        
        


    
    
    
    



            
        
        
    
        
        

    





