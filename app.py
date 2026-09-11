import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


st.set_page_config(
    page_title="FoodInsights",
    page_icon="🍔",
    layout="wide"
)


load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@"
    f"{db_host}:{db_port}/{db_name}"
)


st.title("FoodInsights 🍔🥗🍖")
st.subheader("Análise de pedidos de delivery")


query = """
SELECT *
FROM pedidos;
"""

df = pd.read_sql(query, engine)


st.sidebar.header("🔎 Filtros")

cidades = st.sidebar.multiselect(
    "Cidade",
    options=sorted(df["cidade"].dropna().unique()),
    default=sorted(df["cidade"].dropna().unique())
)

categorias = st.sidebar.multiselect(
    "Categoria",
    options=sorted(df["categoria"].dropna().unique()),
    default=sorted(df["categoria"].dropna().unique())
)

status = st.sidebar.multiselect(
    "Status",
    options=sorted(df["status"].dropna().unique()),
    default=sorted(df["status"].dropna().unique())
)


df_filtrado = df[
    df["cidade"].isin(cidades)
    & df["categoria"].isin(categorias)
    & df["status"].isin(status)
]


total_pedidos = len(df_filtrado)
faturamento = df_filtrado["valor_pedido"].sum()
ticket_medio = df_filtrado["valor_pedido"].mean()
tempo_medio = df_filtrado["tempo_entrega_min"].mean()

taxa_cancelamento = (
    (df_filtrado["status"] == "Cancelado").mean() * 100
)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📦 Total de pedidos",
    f"{total_pedidos:,}"
)

col2.metric(
    "💰 Faturamento",
    f"R$ {faturamento:,.2f}"
)

col3.metric(
    "🛒 Ticket médio",
    f"R$ {ticket_medio:,.2f}"
)

col4.metric(
    "🛵 Tempo médio",
    f"{tempo_medio:.1f} min"
)

col5.metric(
    "❌ Cancelamentos",
    f"{taxa_cancelamento:.2f}%"
)


st.divider()


st.subheader("💰 Faturamento por categoria")

faturamento_categoria = (
    df_filtrado.groupby("categoria")["valor_pedido"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(faturamento_categoria)


st.subheader("📍 Pedidos por cidade")

pedidos_cidade = df_filtrado["cidade"].value_counts()

st.bar_chart(pedidos_cidade)

st.subheader("🛵 Tempo médio de entrega por cidade")

tempo_cidade = (
    df_filtrado.groupby("cidade")["tempo_entrega_min"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(tempo_cidade)