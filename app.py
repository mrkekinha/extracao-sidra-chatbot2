import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq

from tools.sidra_tool import (
    consultar_sidra,
    listar_campos_da_tabela,
    get_municipios_mg,
    get_cod_estado
)

# Configuração inicial
st.set_page_config(page_title="Chatbot IBGE", layout="wide")
st.title("🤖 Chatbot IBGE com Dados Municipais")

# --- Tabelas disponíveis ---
tabelas_disponiveis = {
    "1419": "Produção de Leite por Município",
    "6579": "População residente por Município",
    "2938": "Produto Interno Bruto dos Municípios",
    "1612": "Efetivo de rebanhos, por tipo de rebanho",
    "5440": "Número de estabelecimentos agropecuários por atividade",
    "7060": "Área plantada e colhida das principais lavouras",
    "2508": "População economicamente ativa por município",
    "1620": "Produção de ovos de galinha",
    "1398": "Produção de cana-de-açúcar",
}

# --- Sidebar ---
with st.sidebar:
    st.header("🔍 Parâmetros de consulta")
    tabela_nome = st.selectbox("Escolha a tabela:", options=list(tabelas_disponiveis.values()))
    tabela_num = [k for k, v in tabelas_disponiveis.items() if v == tabela_nome][0]

    nivel = st.radio("Escolha o nível territorial:", ["municipal", "estadual"])

    if nivel == "municipal":
        municipios = get_municipios_mg()
        local = st.selectbox("Município (MG):", options=municipios)
        local_param = municipios[local]
    else:
        local = st.text_input("Estado (nome ou código IBGE):", placeholder="Ex: Minas Gerais ou 31")
        local_param = get_cod_estado(local)

    variaveis = st.text_input("Códigos das variáveis (opcional):", placeholder="Ex: 37, 593")

    col1, col2 = st.columns(2)
    with col1:
        consultar = st.button("🔎 Consultar")
    with col2:
        ver_campos = st.button("📄 Ver variáveis disponíveis")

# --- Mostrar campos disponíveis da tabela ---
if ver_campos:
    st.info(f"🔍 Variáveis disponíveis na tabela {tabela_num}: {tabela_nome}")
    try:
        campos = listar_campos_da_tabela(tabela_num)
        for campo in campos:
            st.markdown(f"- {campo}")
    except Exception as e:
        st.error(f"Erro ao listar campos: {e}")

# --- Executar consulta ao SIDRA ---
if consultar:
    st.subheader("📊 Resultado da Consulta")

    try:
        df = consultar_sidra(tabela_num, nivel, local_param, variaveis)
        st.dataframe(df)

        # Gráfico automático
        st.subheader("📈 Gráfico")
        colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns
        if len(colunas_numericas) >= 1:
            col_grafico = st.selectbox("Coluna para o gráfico:", options=colunas_numericas)
            fig = px.bar(df, x=df.columns[0], y=col_grafico, title=f"Gráfico de {col_grafico}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há colunas numéricas suficientes para gerar gráfico.")

    except Exception as e:
        st.error(f"❌ Erro ao consultar o SIDRA: {e}")
        st.markdown("💡 **Dicas:**")
        st.markdown("- Verifique se o número da tabela está correto;")
        st.markdown("- Informe corretamente 'municipal' ou 'estadual';")
        st.markdown("- Verifique o nome ou código do município/estado (ex: '3106200' para BH);")
        st.markdown("- Use 'all' para consultar todos os locais.")

# --- Agente LangChain integrado ---
st.divider()
st.header("🧠 Chat com o Assistente IBGE")

# Define as ferramentas (tools) que o agente pode usar
tools = [
    Tool.from_function(
        name="Consulta SIDRA",
        func=consultar_sidra,
        description="Consulta dados do SIDRA. Argumentos: tabela (str), nivel (municipal ou estadual), local (str), variaveis (str ou vazio)."
    ),
    Tool.from_function(
        name="Listar campos da tabela",
        func=listar_campos_da_tabela,
        description="Lista os campos disponíveis de uma tabela do SIDRA. Argumento: tabela (str)"
    )
]

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key is None:
    raise ValueError("❌ A variável de ambiente GROQ_API_KEY não foi encontrada. Verifique seu arquivo .env")

llm = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
    groq_api_key=groq_api_key
)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Caixa de entrada do usuário
pergunta = st.text_input("Digite sua pergunta para o assistente:", placeholder="Ex: Quais os campos da tabela 2938?")

if pergunta:
    with st.spinner("Consultando agente..."):
        resposta = agent.run(pergunta)
        st.success("✅ Resposta do assistente:")
        st.write(resposta)