import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
import base64


# Criando DataFrames de exemplo (substitua isso pelos seus DataFrames reais)
data1 = {'Coluna_A': [1, 2, 3], 'Coluna_B': ['01/01/2023', '01/03/2023', '01/06/2023'], 'Coluna_C': ['', '', '']}
data2 = {'Coluna_A': [4, 5, 6], 'Coluna_B': ['01/09/2023', '01/12/2023', '01/01/2024'], 'Coluna_C': ['', '', '']}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Converter a coluna 'date' para datetime64
df1['Coluna_B'] = pd.to_datetime(df1['Coluna_B'], format='%d/%m/%Y')  # Corrigir o formato aqui
df2['Coluna_B'] = pd.to_datetime(df2['Coluna_B'], format='%d/%m/%Y')  # Corrigir o formato aqui

# Adicionando a coluna 'Origem' para identificar a origem dos dados
df1['Origem'] = 'df1'
df2['Origem'] = 'df2'

# Concatenando os DataFrames
df_concatenado = pd.concat([df1, df2], ignore_index=True)

# Criando um DataFrame temporário sem a coluna 'Origem'
df_final = df_concatenado.drop(columns=['Origem'])

# Criando um DataFrame temporário sem a coluna 'Origem'
df_final2 = df2.drop(columns=['Origem'])

# Configurar o app Streamlit
st.title('Teste funcional SCORE')
st.write('Selecione as datas para filtrar o DataFrame.')

# Adicionar widgets para selecionar datas lado a lado
col1, col2 = st.columns(2)

with col1:
    start_date = pd.to_datetime(st.date_input('Data de início',
                                              min_value=df_final['Coluna_B'].min().date(),
                                              max_value=df_final['Coluna_B'].max().date(),
                                              value=df_final['Coluna_B'].min().date()))

with col2:
    end_date = pd.to_datetime(st.date_input('Data de término',
                                            min_value=df_final['Coluna_B'].min().date(),
                                            max_value=df_final['Coluna_B'].max().date(),
                                            value=df_final['Coluna_B'].max().date()))

# Adicionar input para o multiplicador (número decimal)
multiplicador = st.number_input('Multiplicador para conversão de moeda', min_value=0.01, value=1.0,
                                placeholder="Digite um número...", format="%.2f")

# Cria um toggle com o texto "Manipular dataframe"
toggle = st.toggle("Resumir relatório")

# Obtém a data de hoje
data_de_hoje = datetime.today().strftime('%Y-%m-%d')

# Define o nome do arquivo Excel baseado no estado do toggle
if toggle:
    excel_file_name = f"Summary-PO-Report-{data_de_hoje}.xlsx"
else:
    excel_file_name = f"Complete-PO-Report-{data_de_hoje}.xlsx"

if toggle:
    # Filtrar e exibir o DataFrame
    filtered_df2 = df_final2.loc[(df_final2['Coluna_B'] >= start_date) & (df_final2['Coluna_B'] <= end_date)]

    # Formatar a coluna 'date' para exibir apenas a data
    filtered_df2['Coluna_B'] = filtered_df2['Coluna_B'].dt.strftime('%d/%m/%Y')

    # Multiplicar Coluna_A pelo multiplicador (conversão de moeda)
    filtered_df2['Coluna_C'] = filtered_df2['Coluna_A'] * multiplicador

    # Renomear colunas
    filtered_df2 = filtered_df2.rename(columns={'Coluna_A': 'Numero', 'Coluna_B': 'Data', 'Coluna_C': 'Multiplicado'})

    # Exibindo o DataFrame 'df2' no Streamlit com todas as linhas em lightblue
    st.dataframe(filtered_df2.style.apply(lambda x: ['background-color: lightblue' for i in x], axis=1))

else:
    # Filtrar e exibir o DataFrame
    filtered_df = df_final.loc[(df_final['Coluna_B'] >= start_date) & (df_final['Coluna_B'] <= end_date)]

    # Formatar a coluna 'date' para exibir apenas a data
    filtered_df['Coluna_B'] = filtered_df['Coluna_B'].dt.strftime('%d/%m/%Y')

    # Multiplicar Coluna_A pelo multiplicador (conversão de moeda)
    filtered_df['Coluna_C'] = filtered_df['Coluna_A'] * multiplicador

    # Renomear colunas
    filtered_df = filtered_df.rename(columns={'Coluna_A': 'Numero', 'Coluna_B': 'Data', 'Coluna_C': 'Multiplicado'})

    # Exibindo o DataFrame no Streamlit e aplicando estilos usando o DataFrame original
    st.dataframe(filtered_df.style.apply(lambda x: ['background-color: lightblue' if df_concatenado['Origem'][
                                                                      x.name] == 'df2' else '' for i in x], axis=1))

# Cria um botão para download do DataFrame em Excel
if st.button('Baixar DataFrame em Excel'):
    # Codifica o conteúdo do arquivo em bytes
    if toggle:
        filtered_df2.to_excel(excel_file_name, index=False, engine='openpyxl')
        success_message = f'O DataFrame df2 foi baixado em formato Excel. [Clique aqui para baixar]({excel_file_name})'
        # Exibe o link de download
        st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(open(excel_file_name, "rb").read()).decode()}" download="{excel_file_name}">Clique aqui para baixar</a>', unsafe_allow_html=True)
    else:
        filtered_df.to_excel(excel_file_name, index=False, engine='openpyxl')
        success_message = f'O DataFrame final foi baixado em formato Excel. [Clique aqui para baixar]({excel_file_name})'
        # Exibe o link de download
        st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(open(excel_file_name, "rb").read()).decode()}" download="{excel_file_name}">Clique aqui para baixar</a>', unsafe_allow_html=True)
