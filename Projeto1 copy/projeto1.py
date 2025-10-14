# ============================================================
# Importação das bibliotecas necessárias
# ============================================================

import pandas as pd              # Biblioteca para manipulação e leitura de dados em tabelas (Excel, CSV, etc.)
import matplotlib.pyplot as plt  # Biblioteca para gerar gráficos e visualizações
import numpy as np               # Biblioteca para operações numéricas e manipulação de arrays

# ============================================================
# Função: conta_ocorrencias
# Objetivo: contar quantas vezes cada valor aparece em cada coluna da matriz
# ============================================================

def conta_ocorrencias(matriz):
    # Converte a lista de listas (matriz) para um array NumPy genérico (permite misturar texto e números)
    matriz = np.array(matriz, dtype=np.uint16)

    listaContador = []  # Lista onde ficará um dicionário de contagens para cada coluna
    alfabetos = []      # Lista com os valores únicos (alfabeto) de cada coluna

    # Percorre todas as colunas da matriz (pelo número de colunas)
    for i in range(matriz.shape[1]):
        coluna = matriz[:, i]  # Seleciona a coluna i

        # np.unique devolve os valores únicos e as suas contagens
        valores, contagens = np.unique(coluna, return_counts=True)

        # Cria um dicionário {valor: contagem} para essa coluna e guarda
        listaContador.append(dict(zip(valores, contagens)))

        # Guarda também os valores únicos (alfabeto dessa coluna)
        alfabetos.append(valores)

    # Retorna a lista de contagens e os alfabetos
    return listaContador, alfabetos


# ============================================================
# Função: plot_mpg_scatter
# Objetivo: gerar gráficos de dispersão (scatter plots)
#           relacionando "MPG" com outras variáveis do dataset
# ============================================================

def plot_mpg_scatter(data, varNames):
    plt.close('all')  # Fecha quaisquer janelas de gráficos antigas (limpeza de estado)
    fig = plt.subplots(3, 2, figsize=(10, 10))  # Cria uma figura com 3 linhas e 2 colunas de subplots

    # Percorre todas as variáveis menos a última (para evitar "MPG vs MPG")
    for i in range(len(varNames) - 1):
        plt.subplot(3, 2, i + 1)  # Define a posição do subplot atual
        plt.scatter(data[varNames[i]], data['MPG'], c="#C50404")  # Cria o gráfico de dispersão
        plt.title(f"MPG vs {varNames[i]}")  # Título do gráfico
        plt.xlabel(varNames[i])              # Nome do eixo X
        plt.ylabel('MPG')                    # Nome do eixo Y

        # Configura os eixos para mostrar apenas números inteiros 
        '''O “locator” diz ao Matplotlib onde colocar as marcas principais (ticks) no eixo.
            Podes definir tu mesmo, ou usar uma classe automática — como a MaxNLocator.
            --plt.MaxNLocator(integer=True)
            Este é o tipo de locator que controla o espaçamento das marcas.
            O argumento integer=True diz:
            “coloca apenas marcas em valores inteiros (sem números decimais).”'''
        
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.tight_layout()  # Ajusta os espaçamentos entre gráficos para não se sobreporem
    plt.show()          # Mostra todos os gráficos na janela


# ============================================================
# Função principal: main
# Objetivo: carregar os dados, processá-los e mostrar resultados
# ============================================================

def main():
    # Caminho para o ficheiro Excel com os dados do dataset
    path = '/Users/manuelgallo/Documents/Universidade/2º ANO/TI/Projeto1/CarDataset.xlsx'

    # Lê o ficheiro Excel para um DataFrame do pandas
    data = pd.read_excel(path)

    # Converte o DataFrame para uma lista de listas (para a função de contagem)
    matriz = data.values.tolist()

    # Obtém a lista com os nomes das colunas (variáveis)
    varNames = data.columns.values.tolist()

    # Chama a função que conta as ocorrências de cada valor em cada coluna
    listaContador, alfabetos = conta_ocorrencias(matriz)

    # ============================================================
    # Impressão da matriz (tabela original dos dados)
    # ============================================================

    print("\n=== MATRIZ DE DADOS ===")
    for linha in matriz:
        print("\n", linha)

    # ============================================================
    # Impressão das contagens de ocorrências por coluna
    # ============================================================

    for i in range(len(listaContador)):
        print(f"\n=== Contagem de símbolos para {varNames[i]} ===")
        for valor, contagem in listaContador[i].items():
            print(f"{valor}: {contagem}")

    # Gera e mostra os gráficos de dispersão
    plot_mpg_scatter(data, varNames)

    # Retorna as contagens e alfabetos (caso se queira usar depois)
    return listaContador, alfabetos


# ============================================================
# Execução do programa (ponto de entrada)
# ============================================================

# Ao correr o ficheiro, chama a função principal
listaContador, alfabetos = main()
