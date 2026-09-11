import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from groq import Groq


st.set_page_config(
    page_title="FoodInsights",
    page_icon="🍔",
    layout="wide"
)


load_dotenv()

try:
    supabase_url = st.secrets["SUPABASE_DATABASE_URL"]
    groq_api_key = st.secrets["GROQ_API_KEY"]

except Exception:
    supabase_url = os.getenv("SUPABASE_DATABASE_URL")
    groq_api_key = os.getenv("GROQ_API_KEY")


if not supabase_url:
    st.error("Conexão com o banco de dados não configurada.")
    st.stop()

if not groq_api_key:
    st.error("Chave da API de IA não configurada.")
    st.stop()


engine = create_engine(
    supabase_url,
    connect_args={"sslmode": "require"}
)

client = Groq(api_key=groq_api_key)


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


st.divider()


st.subheader("✨ Insights com Inteligência Artificial")

if st.button("✨ Gerar insights com IA"):

    resumo_dados = f"""
    Total de pedidos: {total_pedidos}
    Faturamento: R$ {faturamento:.2f}
    Ticket médio: R$ {ticket_medio:.2f}
    Tempo médio de entrega: {tempo_medio:.2f} minutos
    Taxa de cancelamento: {taxa_cancelamento:.2f}%

    Faturamento por categoria:
    {faturamento_categoria.to_string()}

    Pedidos por cidade:
    {pedidos_cidade.to_string()}

    Tempo médio de entrega por cidade:
    {tempo_cidade.to_string()}
    """

    prompt = f"""
    Você é um analista de dados especializado em delivery.

    Analise os indicadores abaixo e gere insights objetivos
    para apoiar decisões de negócio.

    Identifique:
    1. Principais pontos positivos.
    2. Possíveis problemas ou pontos de atenção.
    3. Tendências relevantes.
    4. Duas sugestões práticas de melhoria.

    Não invente informações que não estejam presentes nos dados.

    Dados:
    {resumo_dados}
    """

    with st.spinner("Analisando os dados..."):

        resposta = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )

    insight = resposta.choices[0].message.content

    st.markdown(insight)