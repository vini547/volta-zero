import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

sns.set_theme(style="ticks", rc={"axes.spines.right": False, "axes.spines.top": False})

def multiselect_filter(df, col, selected):
    if 'all' in selected:
        return df
    return df[df[col].isin(selected)].reset_index(drop=True)

@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    return output.getvalue()

def main():
    st.set_page_config(page_title='Telemarketing Analysis',
                       page_icon='M19 Pratique 1/img/telmarketing_icon.png',
                       layout="wide")

    st.title('📊 Telemarketing Analysis')
    st.markdown("---")

    st.sidebar.image(Image.open("M19 Pratique 1/img/Bank-Branding.jpg"))
    data_file = st.sidebar.file_uploader("📁 Suba o arquivo", type=['csv', 'xlsx'])

    if data_file:
        try:
            if data_file.name.endswith('.csv'):
                bank_raw = pd.read_csv(data_file, sep=';')
            else:
                bank_raw = pd.read_excel(data_file)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return

        bank = bank_raw.copy()
        st.subheader('📋 Antes dos filtros')
        st.dataframe(bank_raw.head())

        with st.sidebar.form(key='form_filtros'):
            min_age, max_age = int(bank.age.min()), int(bank.age.max())
            idades = st.slider("Idade", min_value=min_age, max_value=max_age, value=(min_age, max_age))

            jobs_list = bank.job.unique().tolist()
            jobs_list.append('all')
            jobs_selected = st.multiselect("Profissões", jobs_list, default=['all'])

            submitted = st.form_submit_button("Aplicar Filtros")

        if submitted:
            bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
            bank = multiselect_filter(bank, 'job', jobs_selected)

            st.subheader("📄 Após os filtros")
            st.dataframe(bank.head())

            # Download botão
            df_excel = to_excel(bank)
            st.download_button("📥 Download dados filtrados (.xlsx)",
                               data=df_excel,
                               file_name='bank_filtered.xlsx')

            st.markdown("---")
            st.subheader('📊 Proporção de aceite (target `y`)')

            bank_raw_y = bank_raw['y'].value_counts(normalize=True).mul(100).to_frame(name='percentual')
            bank_raw_y = bank_raw_y.sort_index().reset_index().rename(columns={'index': 'y'})

            bank_y = bank['y'].value_counts(normalize=True).mul(100).to_frame(name='percentual')
            bank_y = bank_y.sort_index().reset_index().rename(columns={'index': 'y'})

            fig, ax = plt.subplots(1, 2, figsize=(10, 4))

            sns.barplot(data=bank_raw_y, x='y', y='percentual', ax=ax[0])
            ax[0].bar_label(ax[0].containers[0])
            ax[0].set_title('Dados Brutos')

            sns.barplot(data=bank_y, x='y', y='percentual', ax=ax[1])
            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title('Dados Filtrados')

            st.pyplot(fig)

if __name__ == '__main__':
    main()
