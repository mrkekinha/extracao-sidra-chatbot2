import requests
from bs4 import BeautifulSoup

def buscar_info_web(termo):
    url = f"https://www.google.com/search?q={termo}+site:ibge.gov.br"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    resposta = requests.get(url, headers=headers)
    soup = BeautifulSoup(resposta.text, "html.parser")

    resultados = soup.find_all("h3")
    if resultados:
        return f"Encontrei algo na web: {resultados[0].text}"
    else:
        return "Não encontrei nada relevante na web."