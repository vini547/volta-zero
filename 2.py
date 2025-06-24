import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(page_title="Filtros Interativos", layout="wide")

# Carregar o dataset
bank_raw = pd.read_csv('M19 Pratique 1/data/input/bank-additional-full.csv', sep=';')
bank = bank_raw.copy()

# Filtro por idade
min_age = int(bank.age.min())
max_age = int(bank.age.max())
age_range = st.slider('Selecione a faixa etária:', min_age, max_age, (25, 50))

bank = bank[(bank['age'] >= age_range[0]) & (bank['age'] <= age_range[1])]

# Filtro por profissão
jobs_list = bank_raw['job'].unique().tolist()
jobs_list.append('all')
jobs_selected = st.multiselect('Selecione a(s) profissão(ões):', jobs_list, default=['all'])

if 'all' not in jobs_selected:
    bank = bank[bank['job'].isin(jobs_selected)]

# Gerar dados de proporção da variável alvo
bank_raw_target = bank_raw['y'].value_counts(normalize=True).to_frame() * 100
bank_raw_target = bank_raw_target.sort_index()
bank_raw_target.columns = ['percent']
bank_raw_target.reset_index(inplace=True)

bank_target = bank['y'].value_counts(normalize=True).to_frame() * 100
bank_target = bank_target.sort_index()
bank_target.columns = ['percent']
bank_target.reset_index(inplace=True)

# Visualização lado a lado
fig, ax = plt.subplots(1, 2, figsize=(10, 4))

sns.barplot(x='y', y='percent', data=bank_raw_target, ax=ax[0])
ax[0].bar_label(ax[0].containers[0])
ax[0].set_title('Original')

sns.barplot(x='y', y='percent', data=bank_target, ax=ax[1])
ax[1].bar_label(ax[1].containers[0])
ax[1].set_title('Filtrado')

st.pyplot(fig)
