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

# Filtrar apenas furtos da cidade Pouso Alegre (ajuste se o nome for diferente)
cidade = "Pouso Alegre"
df_pa = df[df['Cidade'].str.strip().str.upper() == cidade.upper()]

# Contar furtos por bairro e pegar os 10 maiores
furtos_bairros = df_pa['Bairro'].value_counts().head(10)

# Exibir tabela
st.subheader("Top 10 bairros com mais furtos")
st.table(furtos_bairros)

# Gráfico de barras
st.subheader("Gráfico de barras - Furtos por bairro")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=furtos_bairros.values, y=furtos_bairros.index, palette="viridis", ax=ax)
ax.set_xlabel("Número de furtos")
ax.set_ylabel("Bairro")
st.pyplot(fig)

# Gráfico pizza
st.subheader("Gráfico de pizza - Percentual de furtos por bairro")
fig2, ax2 = plt.subplots()
ax2.pie(furtos_bairros.values, labels=furtos_bairros.index, autopct='%1.1f%%', startangle=140)
ax2.axis('equal')  # para círculo perfeito
st.pyplot(fig2)
