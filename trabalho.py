import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Análise de Furtos em Pouso Alegre")

# Caminho do arquivo CSV
caminho_arquivo = "Alvos - Furto - Jan 2022 a Abr 2025.csv"

@st.cache_data
def carregar_dados():
    df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()
    df_pa = df[df["Município"].str.upper() == "POUSO ALEGRE"]
    df_pa.loc[:, "Data Fato"] = pd.to_datetime(df_pa["Data Fato"], errors="coerce")
    df_pa = df_pa[~df_pa["Bairro - FATO FINAL"].str.upper().isin(["DESCONHECIDO", "NÃO CADASTRADO", ""])]
    df_pa['Ano Fato'] = df_pa['Data Fato'].dt.year
    return df_pa

df_pa = carregar_dados()

# Top 10 bairros com mais furtos automaticamente
top_bairros = df_pa["Bairro - FATO FINAL"].value_counts().head(10)
st.header("Top 10 Bairros com Mais Furtos")
st.write(top_bairros)

# Gráfico de pizza dos 10 bairros
fig1, ax1 = plt.subplots()
top_bairros.plot.pie(
    autopct='%1.1f%%',
    startangle=90,
    shadow=True,
    ax=ax1,
    textprops={'fontsize': 6}  # diminui tamanho do texto
)
ax1.set_ylabel('')
ax1.set_title('Top 10 Bairros com Mais Furtos - Pouso Alegre')
st.pyplot(fig1)

# Gráfico de barras: furtos por ano (todos os bairros)
st.header("Evolução dos Furtos por Ano")
furtos_por_ano = df_pa["Ano Fato"].value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=furtos_por_ano.index.astype(str), y=furtos_por_ano.values, ax=ax2)
ax2.set_xlabel('Ano')
ax2.set_ylabel('Quantidade de Furtos')
ax2.set_title('Evolução dos Furtos por Ano - Pouso Alegre')
plt.xticks(rotation=45)
st.pyplot(fig2)

# Evolução dos furtos ao longo dos anos para os 10 bairros top
df_top10 = df_pa[df_pa["Bairro - FATO FINAL"].isin(top_bairros.index)]

furtos_por_ano_bairro = (
    df_top10
    .groupby(['Ano Fato', 'Bairro - FATO FINAL'])
    .size()
    .reset_index(name='Quantidade')
)

fig3, ax3 = plt.subplots(figsize=(12, 8))
sns.lineplot(
    data=furtos_por_ano_bairro,
    x='Ano Fato',
    y='Quantidade',
    hue='Bairro - FATO FINAL',
    marker="o",
    ax=ax3
)
ax3.set_title("Evolução dos Furtos por Ano nos 10 Bairros com Mais Furtos - Pouso Alegre")
ax3.set_xlabel("Ano")
ax3.set_ylabel("Quantidade de Furtos")
ax3.legend(title='Bairros', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig3)
