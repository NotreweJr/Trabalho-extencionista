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
    
    # Conferir colunas existentes
    if "Data Fato" not in df.columns:
        st.error("Coluna 'Data Fato' não encontrada no dataset.")
        return pd.DataFrame()  # Retorna dataframe vazio
    
    # Converter 'Data Fato' para datetime, ignorando erros
    df["Data Fato"] = pd.to_datetime(df["Data Fato"], errors="coerce")
    
    # Filtrar município
    df_pa = df[df["Município"].str.upper() == "POUSO ALEGRE"]
    
    # Filtrar bairros válidos (ajuste o nome exato da coluna de bairro)
    bairro_col = "Bairro - FATO FINAL"
    if bairro_col not in df_pa.columns:
        st.error(f"Coluna '{bairro_col}' não encontrada no dataset.")
        return pd.DataFrame()
    
    df_pa = df_pa[~df_pa[bairro_col].str.upper().isin(["DESCONHECIDO", "NÃO CADASTRADO", ""])]
    
    # Remover linhas sem data válida
    df_pa = df_pa[df_pa["Data Fato"].notna()]
    
    # Criar coluna 'Ano Fato'
    df_pa['Ano Fato'] = df_pa['Data Fato'].dt.year
    
    return df_pa

df_pa = carregar_dados()
if df_pa.empty:
    st.stop()

st.header("Top 10 Bairros com Mais Furtos")
top_bairros = df_pa["Bairro - FATO FINAL"].value_counts().head(10)
st.write(top_bairros)

# Total geral dos furtos nesses top 10 bairros
total_furtos = top_bairros.sum()
st.write(f"Total de furtos nos top 10 bairros: {total_furtos}")

# Gráfico de pizza com tamanho de fonte menor
fig1, ax1 = plt.subplots()
top_bairros.plot.pie(
    autopct='%1.1f%%',
    startangle=90,
    shadow=True,
    ax=ax1,
    textprops={'fontsize': 6}
)
ax1.set_ylabel('')
ax1.set_title('Top 10 Bairros com Mais Furtos - Pouso Alegre')
st.pyplot(fig1)

# Evolução dos furtos por ano para os top 10 bairros
st.header("Evolução dos Furtos por Ano para os Top 10 Bairros")

# Filtra o dataframe para os top 10 bairros
df_top_bairros = df_pa[df_pa["Bairro - FATO FINAL"].isin(top_bairros.index)]

# Agrupa por ano e bairro, conta furtos
evolucao = df_top_bairros.groupby(['Ano Fato', 'Bairro - FATO FINAL']).size().unstack(fill_value=0)

# Plota gráfico de linhas
fig2, ax2 = plt.subplots(figsize=(12, 6))
evolucao.plot(ax=ax2, marker='o')
ax2.set_xlabel('Ano')
ax2.set_ylabel('Quantidade de Furtos')
ax2.set_title('Evolução dos Furtos por Ano - Top 10 Bairros')
plt.xticks(rotation=45)
plt.legend(title='Bairros', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig2)
