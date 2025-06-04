import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(layout="centered")
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
    if "Ano Fato" not in df_pa.columns:
        df_pa["Ano Fato"] = df_pa["Data Fato"].dt.year
    return df_pa

df_pa = carregar_dados()

# -----------------------------------
# Top 10 bairros com mais furtos + TOTAL
# -----------------------------------
st.header("Top 10 Bairros com Mais Furtos")

# Top 10 bairros
top_bairros = df_pa["Bairro - FATO FINAL"].str.upper().value_counts().head(10)

# Adiciona linha TOTAL usando concat
top_bairros_com_total = pd.concat([
    top_bairros,
    pd.Series({"TOTAL": top_bairros.sum()})
])

# Exibe a tabela com total
st.write("**Total de furtos nos 10 bairros mais afetados:**")
st.dataframe(top_bairros_com_total.rename_axis("Bairro").reset_index(name="Furtos"), use_container_width=True)

# Gráfico de pizza
fig1, ax1 = plt.subplots(figsize=(6, 6))
top_bairros.plot.pie(
    autopct='%1.1f%%',
    startangle=90,
    shadow=False,
    ax=ax1,
    textprops={'fontsize': 8}
)
ax1.set_ylabel('')
ax1.set_title('Top 10 Bairros com Mais Furtos', fontsize=12)
st.pyplot(fig1)

# -----------------------------------
# Evolução dos furtos por ano
# -----------------------------------
st.header("Evolução dos Furtos por Ano")
furtos_por_ano = df_pa["Ano Fato"].value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(x=furtos_por_ano.index.astype(str), y=furtos_por_ano.values, ax=ax2)
ax2.set_xlabel('Ano', fontsize=10)
ax2.set_ylabel('Quantidade de Furtos', fontsize=10)
ax2.set_title('Evolução dos Furtos por Ano - Pouso Alegre', fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig2)

# -----------------------------------
# Evolução dos furtos nos 10 bairros
# -----------------------------------
st.header("Evolução dos Furtos por Bairro (Top 10)")

bairros_top10 = [
    "CENTRO", "SAO GERALDO", "JARDIM OLIMPICO", "CRUZEIRO", "FOCH",
    "SAO JOAO", "ARVORE GRANDE", "PRIMAVERA", "SAO CARLOS", "FATIMA I"
]

# Filtrar dados dos top 10 bairros
df_top_bairros = df_pa[df_pa["Bairro - FATO FINAL"].str.upper().isin(bairros_top10)]

# Agrupar por ano e bairro
evolucao = df_top_bairros.groupby(
    [df_top_bairros["Ano Fato"], df_top_bairros["Bairro - FATO FINAL"].str.upper()]
).size().unstack(fill_value=0)

# Gráfico de linha
fig3, ax3 = plt.subplots(figsize=(10, 6))
evolucao.plot(ax=ax3, marker='o')

ax3.set_title("Evolução Anual dos Furtos por Bairro - Pouso Alegre", fontsize=12)
ax3.set_xlabel("Ano", fontsize=10)
ax3.set_ylabel("Quantidade de Furtos", fontsize=10)
ax3.legend(title="Bairro", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
plt.xticks(rotation=45)
st.pyplot(fig3)

# -----------------------------------
# Horários de pico dos furtos
# -----------------------------------
st.header("Horários de Pico dos Furtos")

# Função para extrair hora corretamente
def extrair_hora(valor):
    try:
        if pd.isna(valor):
            return None
        valor = str(valor).strip().zfill(4)  # Ex: 815 -> "0815"
        hora = int(valor[:2])
        if 0 <= hora <= 23:
            return hora
    except:
        return None
    return None

# Aplica a função
df_pa["Hora Fato"] = df_pa["Horário Fato"].apply(extrair_hora)

# Conta furtos por hora
furtos_por_hora = df_pa["Hora Fato"].value_counts().sort_index()

# Gráfico de barras dos horários de pico
fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.barplot(x=furtos_por_hora.index, y=furtos_por_hora.values, ax=ax4, color='salmon')
ax4.set_xlabel("Hora do Dia", fontsize=10)
ax4.set_ylabel("Quantidade de Furtos", fontsize=10)
ax4.set_title("Furtos por Hora do Dia - Pouso Alegre", fontsize=12)
plt.xticks(range(0, 24))
st.pyplot(fig4)
