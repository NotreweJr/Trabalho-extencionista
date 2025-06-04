import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="centered")
st.title("Análise de Furtos em Pouso Alegre")

caminho_arquivo = "Alvos - Furto - Jan 2022 a Abr 2025.csv"

@st.cache_data
def carregar_dados():
    df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()
    df_pa = df[df["Município"].str.upper() == "POUSO ALEGRE"]
    df_pa.loc[:, "Data Fato"] = pd.to_datetime(df_pa["Data Fato"], errors="coerce")
    df_pa = df_pa.dropna(subset=["Data Fato"])  # Remove linhas com data inválida
    df_pa = df_pa[~df_pa["Bairro - FATO FINAL"].str.upper().isin(["DESCONHECIDO", "NÃO CADASTRADO", ""])]
    if "Ano Fato" not in df_pa.columns:
        df_pa["Ano Fato"] = df_pa["Data Fato"].dt.year
    return df_pa

df_pa = carregar_dados()

# Top 10 bairros
st.header("Top 10 Bairros com Mais Furtos")
top_bairros = df_pa["Bairro - FATO FINAL"].str.upper().value_counts().head(10)
top_bairros_com_total = pd.concat([top_bairros, pd.Series({"TOTAL": top_bairros.sum()})])
st.write("**Total de furtos nos 10 bairros mais afetados:**")
st.dataframe(top_bairros_com_total.rename_axis("Bairro").reset_index(name="Furtos"), use_container_width=True)

fig1, ax1 = plt.subplots(figsize=(6, 6))
top_bairros.plot.pie(autopct='%1.1f%%', startangle=90, shadow=False, ax=ax1, textprops={'fontsize': 8})
ax1.set_ylabel('')
ax1.set_title('Top 10 Bairros com Mais Furtos', fontsize=12)
st.pyplot(fig1)

# Evolução anual
st.header("Evolução dos Furtos por Ano")
furtos_por_ano = df_pa["Ano Fato"].value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(x=furtos_por_ano.index.astype(str), y=furtos_por_ano.values, ax=ax2)
ax2.set_xlabel('Ano', fontsize=10)
ax2.set_ylabel('Quantidade de Furtos', fontsize=10)
ax2.set_title('Evolução dos Furtos por Ano - Pouso Alegre', fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig2)

# Evolução por bairro (top 10)
st.header("Evolução dos Furtos por Bairro (Top 10)")
bairros_top10 = [
    "CENTRO", "SAO GERALDO", "JARDIM OLIMPICO", "CRUZEIRO", "FOCH",
    "SAO JOAO", "ARVORE GRANDE", "PRIMAVERA", "SAO CARLOS", "FATIMA I"
]
df_top_bairros = df_pa[df_pa["Bairro - FATO FINAL"].str.upper().isin(bairros_top10)]
evolucao = df_top_bairros.groupby(
    [df_top_bairros["Ano Fato"], df_top_bairros["Bairro - FATO FINAL"].str.upper()]
).size().unstack(fill_value=0)
fig3, ax3 = plt.subplots(figsize=(10, 6))
evolucao.plot(ax=ax3, marker='o')
ax3.set_title("Evolução Anual dos Furtos por Bairro - Pouso Alegre", fontsize=12)
ax3.set_xlabel("Ano", fontsize=10)
ax3.set_ylabel("Quantidade de Furtos", fontsize=10)
ax3.legend(title="Bairro", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
plt.xticks(rotation=45)
st.pyplot(fig3)

# Horários de pico
st.header("Horários de Pico dos Furtos")
def extrair_hora(valor):
    try:
        if pd.isna(valor):
            return None
        valor = str(valor).strip().zfill(4)
        hora = int(valor[:2])
        if 0 <= hora <= 23:
            return hora
    except:
        return None
    return None
df_pa["Hora Fato"] = df_pa["Horário Fato"].apply(extrair_hora)
furtos_por_hora = df_pa["Hora Fato"].value_counts().sort_index()
fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.barplot(x=furtos_por_hora.index, y=furtos_por_hora.values, ax=ax4, color='salmon')
ax4.set_xlabel("Hora do Dia", fontsize=10)
ax4.set_ylabel("Quantidade de Furtos", fontsize=10)
ax4.set_title("Furtos por Hora do Dia - Pouso Alegre", fontsize=12)
plt.xticks(range(0, 24))
st.pyplot(fig4)

# Furtos por dia da semana
st.header("Furtos por Dia da Semana")
df_pa["Dia da Semana"] = df_pa["Data Fato"].dt.day_name(locale='pt_BR')
ordem_dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
furtos_por_dia = df_pa["Dia da Semana"].value_counts().reindex(ordem_dias)
fig_dia, ax_dia = plt.subplots()
sns.barplot(x=furtos_por_dia.index.str.capitalize(), y=furtos_por_dia.values, ax=ax_dia, palette="Blues_r")
ax_dia.set_title("Furtos por Dia da Semana")
ax_dia.set_ylabel("Quantidade de Furtos")
ax_dia.set_xlabel("Dia da Semana")
plt.xticks(rotation=45)
st.pyplot(fig_dia)

# Linha do tempo mensal
st.header("Furtos por Mês")
df_pa["Ano-Mes"] = df_pa["Data Fato"].dt.to_period("M").astype(str)
furtos_mensais = df_pa["Ano-Mes"].value_counts().sort_index()
fig_mes, ax_mes = plt.subplots(figsize=(12, 4))
sns.lineplot(x=furtos_mensais.index, y=furtos_mensais.values, marker='o', ax=ax_mes)
ax_mes.set_title("Furtos por Mês")
ax_mes.set_xlabel("Mês")
ax_mes.set_ylabel("Ocorrências")
plt.xticks(rotation=45)
st.pyplot(fig_mes)

# Tipo de local mais visado (coluna "Descrição Local Imediato")
if "Descrição Local Imediato" in df_pa.columns:
    st.header("Top 10 Locais mais Visados")
    locais_comuns = df_pa["Descrição Local Imediato"].value_counts().head(10)
    fig_locais, ax_locais = plt.subplots()
    sns.barplot(y=locais_comuns.index, x=locais_comuns.values, ax=ax_locais, palette="OrRd")
    ax_locais.set_title("Top 10 Locais mais Visados")
    ax_locais.set_xlabel("Quantidade de Furtos")
    st.pyplot(fig_locais)
