import matplotlib.pyplot as plt
import streamlit as st
import io
from langchain.tools import tool

@tool
def gerar_grafico(dados: str, titulo: str = "Gráfico") -> str:
    """
    Gera gráfico com base nos dados do SIDRA.
    """
    try:
        plt.figure(figsize=(8, 4))
        plt.plot([1, 2, 3], [10, 20, 15], marker='o')  # Exemplo ilustrativo
        plt.title(titulo)
        st.pyplot(plt)
        return "Gráfico gerado com sucesso."
    except Exception as e:
        return f"Erro ao gerar gráfico: {e}"