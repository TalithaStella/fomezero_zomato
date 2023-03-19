link: https://talithastella-fomezero-zomato.streamlit.app/
<hr>

## 1 Problema de negócio

Trata de uma empresa fictícia com o intúito de aplicar os conhecimentos adquiridos durante o curso de Python da ComunidadeDS. Aqui assumimos que um Marktplace de restaurantes me contratou como Cientista de Dados e minha primeira tarefa é ajudar o CEO a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer utilizando dados afim de ajudar na tomada de melhores decisões estratégicas e alavancar ainda mais a FomeZero. Para isso é preciso que seja feita uma análise nos dados da empresa e que sejam gerados dashboards.

A empresa FomeZero é uma marketplace de restaurantes. Seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero e disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.
<br><br>


## 2. Premissas assumidas para análise

I. O modelo de negócio foi assumido como um marketplace

II. As principais visões de negócio foram: Visão Países, Cidade, Culinária, também com aspecto de restaurantes em cada uma das visões. 

III. A base de dados não contém informações de data, por isso não é possível determinar dimensão temporal.

IV. A base de dados contém diferentes tipos de moedas, por isso para determinar se um prato é considerado caro ou barato foi adotada a variável "Price range", seguindo os seguintes parâmetros:
	- 1: Cheap
	- 2: Nomal
	- 3: Expensive
	- 4: Gourmet
<br><br>

## 3. Estratégia de solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio. As métricas foram decididas pelo CEO da empresa, e com base nelas outras questões foram acrescidas. 

Cada visão é representada pelos seguintes conjunto de métricas: 

### I. Visão Geral
- Restaurantes cadastrados
- Países cadastrados
- Cidades cadastradas
- Total avaliações feitas
- Quantidade de culinárias registradas



### II. Visão Países:
- Paises com mais cidades registradas
- Países que possuem a maior média de avaliações registrada
- Países que possuem mais culinárias distintas?
- Média de custo e de avaliação dos países

#### Visão país/Restaurante:

- Países que possuem mais restaurantes registrados
- Paises com restaurantes mais caros
- Relação de entregas
- Relação de pedidos online
- Relação de reservas



### III. Visão Cidades
- Cidade melhores avaliadas
- Top 5 cidades com mais tipos de culinária distintas
- Top 5 cidades cidades mais caras em geral
- Top 5 cidade mais baratas em geral
- Top 5 cidades mais caras para 2 pessoas
- Top 5 cidades mais baratas para 2 pessoas

#### Visão cidade/restaurantes
- Top 5 cidades com mais restaurantes registrados
- Top 10 cidades com restaurantes com nota média acima de 4
- Top 5 cidades com restaurantes com nota média abaixo de 2.5


### IV. Visão culinárias.
- Diversidade culinária
- Top 10 melhores cozinhas
- Top 10 piores cozinhas
- Top 10 culinárias mais caras e pior avaliada
- Top 10 culinárias mais baratas e melhor avaliada

#### Visão culinária/restaurantes
- Melhor/pior culinária brasileira
- Restaurante da melhor e pior culinária
- Restaurantes com mais e menos votos realizados
- Restaurantes com maior e menor nota média
- Restaurantes mais caros e mais baratos
<br>

## 4. Top 3 Insights de dados

I. Índia lidera em maior número de cidades registradas, maior diversidade culinária e mais restaurantes registrados, além disso tem 5 cidades cadastradas que possuem o menor valor de pratos em geral.

II. Cerca de metade dos restaurantes que aceitam pedidos online fazem entregas.

III. O Brasil é um dos países mais caros em relação à média de avaliação em geral, além disso possui culinária com uma das piores avaliações. 
<br><br>

## 5. O produto final do projeto

Painel interativo online, hospedado em uma Cloud e disponível atravez do link: https://talithastella-fomezero-zomato.streamlit.app/
<br><br>

## 6 Conclusão

O projeto previam 2 objetivos, o primeiro consistia em aplicar os conhecimentos adquiridos durante o curso, sendo os principais: manipulação de dados com Python e bibliotecas relacionadas, ETL, criação de gráficos interativos usando streamlit, resolução de problemas de negócio e visão estratégica.
O segundo objetivo foi criar um conjunto de gráficos e/ou tabelas que ixibissem as métricas da melhor maneira possível, afim de melhorar a tomada de decisão da empresa fictícia. 
<br><br>

## 7 Próximos passos

I. Reduzir o número de métricas
II. Adicionar novas visões de negócio. 
III. Se também tiver índices temporais, adicionar na análise.
