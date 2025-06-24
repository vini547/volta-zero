import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análise Banco", layout="wide")

# Carregar dados
bank = pd.read_csv('M19 Pratique 1/data/input/bank-additional-full.csv', sep=';')
st.title('Análise de Dados - Marketing Bancário')
st.write('Apresentação do dataset:')
st.dataframe(bank.head(10))

# Gráfico com distribuição da variável alvo
st.subheader('Distribuição da variável alvo (y)')
bank_target = bank['y'].value_counts(normalize=True).to_frame() * 100
bank_target = bank_target.sort_index()
bank_target.columns = ['percent']
bank_target.reset_index(inplace=True)

fig, ax = plt.subplots()
sns.barplot(x='y', y='percent', data=bank_target, ax=ax)
ax.bar_label(ax.containers[0])
ax.set_title('Porcentagem por Classe (y)')
st.pyplot(fig)
