import pandas as pd
import plotly.express as px
import streamlit as st
st.header('Registros de Bromeliaceae no Brasil')
st.write('Dados de ocorrência do GBIF para a família Bromeliaceae, '
         'com nomes taxonômicos resolvidos pela Flora e Funga do Brasil.')
Brom_data = pd.read_csv("ocorrencias_bromeliaceae.csv.gz")# lendo os dados

mostrar_dados = st.checkbox('Mostrar tabela de dados')

if mostrar_dados:
    st.write('Amostra dos registros usados nos gráficos:')
    st.dataframe(Brom_data)


hist_button = st.button('Criar histograma') # criar um botão
if hist_button: # se o botão for clicado
    st.subheader('Esforço de coleta ao longo do tempo')
            # escrever uma mensagem
    st.write('Criando um histograma para o conjunto de dados de Registros de espécies de Bromeliaceae')
            
            # criar um histograma
    fig = px.histogram(Brom_data, x="ano",
                   nbins=50, 
                   title="Registros de espécies de Bromeliaceae por ano de coleta", 
                   labels={"ano": "Ano"} ) 
    fig.update_yaxes(title_text="Nº de registros")
        
            # exibir um gráfico Plotly interativo
    st.plotly_chart(fig, use_container_width=True)

disp_button = st.button('Criar dispersão') # criar um botão
if disp_button: # se o botão for clicado
            # escrever uma mensagem
            st.write('Criando um gráfico de dispersão para o conjunto de dados de Registros de espécies de Bromeliaceae')
            
            # criar um grafico de dis
            por_ano = (Brom_data.groupby("ano")
                        .agg(n_registros=("ano", "size"), n_especies=("nome_aceito", "nunique"))
                        .reset_index()
                        .sort_values("ano"))
            fig_disp = px.scatter(por_ano, x="n_registros", y="n_especies",
                                   hover_data=["ano"],
                                   color="ano",
                                     title="Nº de registros × Nº de espécies distintas, por ano",
                                     labels={"n_registros": "Nº de registros no ano", "n_especies": "Nº de espécies distintas no ano"}
                                     )
        
            # exibir um gráfico Plotly interativo
            st.plotly_chart(fig_disp, use_container_width=True)