import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análise de Furtos em Pouso Alegre", layout="wide")
st.title("🔍 Análise de Furtos em Pouso Alegre")
st.markdown("Dados de 2022 até abril de 2025 (fonte: governo estadual)")

@st.cache_data
def carregar_dados():
    caminho_arquivo = "Alvos - Furto - Jan 2022 a Abr 2025.csv"
    df = pd.read_csv(caminho_arquivo, sep=";", encoding="latin1")
    return df

df = carregar_dados()

# Filtrar apenas ocorrências de Pouso Alegre
df_pa = df[df["Município"].str.upper().str.contains("POUSO ALEGRE", na=False)]

# Padronizar nomes de bairro e remover desconhecidos
df_pa["Bairro - FATO FINAL"] = df_pa["Bairro - FATO FINAL"].str.upper().str.strip()
df_pa = df_pa[df_pa["Bairro - FATO FINAL"].notna()]
df_pa = df_pa[~df_pa["Bairro - FATO FINAL"].isin(["NÃO INFORMADO", "DESCONHECIDO", "", "N/I"])]

# Top 10 bairros com mais furtos
top_bairros = df_pa["Bairro - FATO FINAL"].value_counts().head(10)

# Converter data
df_pa["Data Fato"] = pd.to_datetime(df_pa["Data Fato"], errors="coerce")

# Agrupar por ano
df_pa["Ano"] = df_pa["Data Fato"].dt.year
furtos_por_ano = df_pa["Ano"].value_counts().sort_index()

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Top 10 bairros com mais furtos")
    fig1, ax1 = plt.subplots()
    top_bairros.plot.pie(autopct="%1.1f%%", startangle=90, ax=ax1)
    ax1.set_ylabel("")
    st.pyplot(fig1)

with col2:
    st.subheader("📊 Furtos por ano")
    fig2, ax2 = plt.subplots()
    sns.barplot(x=furtos_por_ano.index.astype(str), y=furtos_por_ano.values, palette="crest", ax=ax2)
    ax2.set_ylabel("Quantidade de Furtos")
    ax2.set_xlabel("Ano")
    st.pyplot(fig2)

st.markdown("---")
st.caption("Desenvolvido como parte de um projeto de extensão. Dados públicos do estado.")
