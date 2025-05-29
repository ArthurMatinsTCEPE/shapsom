import streamlit as st
from copy import deepcopy
import plotly.express as px
from page_classes import S1P3_GraficoDispersao
from my_utilities import report_page_top, report_page_bottom, generate_random_string, PAGE_COUNT
from threading import Lock

globals()["lock"] = Lock()

def S1P3_set_default_parameters():
    input_output_columns = list(st.session_state["base reader"].input_columns + st.session_state["base reader"].output_columns)
    st.session_state["variavel_x_dispersao"] = input_output_columns[0]
    st.session_state["variavel_y_dispersao"] = input_output_columns[-1]

def S1P3_load_parameters():
    st.session_state["variavel_x_dispersao"] = st.session_state["grafico dispersao"].variavel_x_dispersao
    st.session_state["variavel_y_dispersao"] = st.session_state["grafico dispersao"].variavel_y_dispersao

def S1P3_update_parameters(variavel_x_dispersao, variavel_y_dispersao):
    st.session_state["grafico dispersao"].variavel_x_dispersao = variavel_x_dispersao
    st.session_state["grafico dispersao"].variavel_y_dispersao = variavel_y_dispersao

report_page_top("grafico dispersao", S1P3_GraficoDispersao, "1. Análise Estatística Exploratória", 3/PAGE_COUNT, set_default_parameters=S1P3_set_default_parameters, load_parameters=S1P3_load_parameters)
st.subheader('Seção 3 - Gráfico de Dispersão')
st.markdown('''O gráfico de dispersão faz parte de uma análise estatística mais ampla apresentada no relatório, que visa 
                explorar a variabilidade e o desempenho geral dos municípios. Ele permite identificar quais municípios
                apresentam desempenhos extremos, tanto positivos quanto negativos, e como os valores da nossa variável alvo estão dispersos
                em relação à media. Esta visualização facilita uma identificação mais superficial das áreas que necessitam de maior atenção e recursos.''')

opcoes = list(st.session_state["base reader"].input_columns + st.session_state["base reader"].output_columns)
nc = st.session_state["base reader"].name_columns[0]

# Seletor para variável do eixo-x
x_var = st.selectbox('Selecione a variável para o eixo X', opcoes, index=opcoes.index(st.session_state["variavel_x_dispersao"]))
# Seletor para variável do eixo-y
y_var = st.selectbox('Selecione a variável para o eixo Y', opcoes, index=opcoes.index(st.session_state["variavel_y_dispersao"]))

with st.spinner('Gerando gráfico de dispersão...'):
    df = deepcopy(st.session_state["base reader"].crunched_database_average)
    dfmc = df.groupby(nc)[[x_var, y_var]].apply(lambda x: x.mode().iloc[0]).reset_index()
    dfmc[dfmc.columns[-1]] = dfmc[dfmc.columns[-1]].round(2)
    
    fig = px.scatter(dfmc, x=x_var, y=y_var, color=y_var, color_continuous_scale='icefire_r')
    fig.update_layout(coloraxis_colorbar=dict(title=None))
    
    st.session_state["grafico dispersao"].map = deepcopy(fig)
    st.plotly_chart(st.session_state["grafico dispersao"].map, use_container_width=True)
    st.info('Gráfico 1 - Gráfico de Dispersão das Variáveis Selecionadas')

report_page_bottom("grafico dispersao", "pages/s1p2_analise_estatistica.py", "pages/s1report.py", update_parameters=lambda : S1P3_update_parameters(x_var, y_var))