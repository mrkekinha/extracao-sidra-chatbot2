import pandas as pd
from sidrapy import get_table
"""
def consultar_sidra(tabela, nivel, local='all', variaveis=None):
    # Tradução do nível territorial
    nivel_territorial = {
        'municipal': 'n6',
        'estadual': 'n2'
    }.get(nivel.lower())

    if not nivel_territorial:
        raise ValueError(f"Nível territorial inválido: {nivel}")

    params = {
        "table_code": tabela,
        "territorial_level": nivel_territorial,
        "ibge_territorial_code": local,
        "variable": variaveis if variaveis else "all",
        "classific": "all",
        "category": "all",
        "period": "last"
    }

    df = get_table(**params)
    return df

"""

def consultar_sidra(tabela, nivel_territorial, localidade, variaveis=None):
    from sidrapy import get_table

    # Mapeando 'municipal' e 'estadual' para os códigos aceitos pelo SIDRA
    if nivel_territorial.lower() == 'municipal':
        nivel_cod = '6'
    elif nivel_territorial.lower() == 'estadual':
        nivel_cod = '3'
    else:
        raise ValueError("Nível territorial inválido. Use 'municipal' ou 'estadual'.")

    # Se o usuário não definir variáveis, usar 'all'
    variaveis = variaveis if variaveis else ['all']

    try:
        df = get_table(
            table_code=tabela,
            territorial_level=nivel_cod,  # Aqui vai o código correto
            ibge_territorial_code=[localidade],
            variable=variaveis,
            classificatory_code='all',
            classificatory_code_value='all',
            period='last'
        )
        return df
    except Exception as e:
        raise RuntimeError(f"Erro ao consultar o SIDRA: {str(e)}")
    
    
def listar_campos_da_tabela(tabela):
    # Exemplo com retorno fixo (idealmente faça scraping ou use API de metadados do SIDRA)
    exemplos = {
        '2938': ['PIB total', 'PIB per capita', 'Valor adicionado', 'Impostos líquidos'],
        '1419': ['Produção de leite', 'Rebanho ordenhado', 'Produtividade'],
        '6579': ['População residente total', 'População urbana', 'População rural']
    }
    return exemplos.get(str(tabela), ['Variáveis não identificadas para esta tabela.'])


def get_municipios_mg():
    return {
        'Belo Horizonte': '3106200',
        'Uberlândia': '3170206',
        'Contagem': '3118601',
        'Juiz de Fora': '3136702',
        'Betim': '3106705',
        'Montes Claros': '3143302',
        'Ribeirão das Neves': '3154606',
        'Ipatinga': '3131307'
        # adicione mais conforme necessário
    }

def get_cod_estado(nome_estado):
    estados = {
        'Acre': '12',
        'Alagoas': '27',
        'Amapá': '16',
        'Amazonas': '13',
        'Bahia': '29',
        'Ceará': '23',
        'Distrito Federal': '53',
        'Espírito Santo': '32',
        'Goiás': '52',
        'Maranhão': '21',
        'Mato Grosso': '51',
        'Mato Grosso do Sul': '50',
        'Minas Gerais': '31',
        'Pará': '15',
        'Paraíba': '25',
        'Paraná': '41',
        'Pernambuco': '26',
        'Piauí': '22',
        'Rio de Janeiro': '33',
        'Rio Grande do Norte': '24',
        'Rio Grande do Sul': '43',
        'Rondônia': '11',
        'Roraima': '14',
        'Santa Catarina': '42',
        'São Paulo': '35',
        'Sergipe': '28',
        'Tocantins': '17'
    }
    return estados.get(nome_estado.strip().title(), nome_estado)