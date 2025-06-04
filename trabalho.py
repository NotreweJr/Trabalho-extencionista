import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Análise de Furtos em Pouso Alegre")

# Caminho do arquivo CSV no seu computador
caminho_arquivo = "Alvos - Furto - Jan 2022 a Abr 2025.csv"

@st.cache_data
def carregar_dados():
    df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()
    df_pa = df[df["Município"].str.upper() == "POUSO ALEGRE"]
    df_pa.loc[:, "Data Fato"] = pd.to_datetime(df_pa["Data Fato"], errors="coerce")
    df_pa = df_pa[~df_pa["Bairro - FATO FINAL"].str.upper().isin(["DESCONHECIDO", "NÃO CADASTRADO", ""])]
    return df_pa

df_pa = carregar_dados()

st.header("Top 10 Bairros com Mais Furtos")
top_bairros = df_pa["Bairro - FATO FINAL"].value_counts().head(10)
st.write(top_bairros)

# Gráfico de pizza
fig1, ax1 = plt.subplots()
top_bairros.plot.pie(
    autopct='%1.1f%%',
    startangle=90,
    shadow=True,
    ax=ax1,
    textprops={'fontsize': 10}  # diminui o tamanho das letras
)
ax1.set_ylabel('')
ax1.set_title('Top 10 Bairros com Mais Furtos - Pouso Alegre')
st.pyplot(fig1)


# Gráfico de barras corrigido (sem palette para evitar warning)
st.header("Evolução dos Furtos por Ano")
furtos_por_ano = df_pa["Ano Fato"].value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=furtos_por_ano.index.astype(str), y=furtos_por_ano.values, ax=ax2)
ax2.set_xlabel('Ano')
ax2.set_ylabel('Quantidade de Furtos')
ax2.set_title('Evolução dos Furtos por Ano - Pouso Alegre')
plt.xticks(rotation=45)
st.pyplot(fig2)
