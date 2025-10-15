import pandas as pd              
import matplotlib.pyplot as plt  
import numpy as np               

def conta_ocorrencias(matriz):
    # Converte a lista de listas (matriz) para um array NumPy genérico (permite misturar texto e números)
    matriz = np.array(matriz, dtype=np.uint16)

    listaContador = []  # lista de um dicionário de contagens para cada coluna
    alfabetos = []      # lista com os valores únicos (alfabeto) de cada coluna

    for i in range(matriz.shape[1]):
        coluna = matriz[:, i]  # Seleciona a coluna i e percorre todas as linhas

        # np.unique devolve os valores únicos e as suas contagens
        valores, contagens = np.unique(coluna, return_counts=True)

        listaContador.append(dict(zip(valores, contagens)))

        alfabetos.append(valores)

    return listaContador, alfabetos

def grafico(data, varNames):
    plt.subplots(3, 2, figsize=(10, 10))  

    for i in range(len(varNames) - 1):
        plt.subplot(3, 2, i + 1)  
        plt.scatter(data[varNames[i]], data['MPG'], c="#C50404")  
        plt.title(f"MPG vs {varNames[i]}")  
        plt.xlabel(varNames[i])             
        plt.ylabel('MPG')                    

        ''' | Parte do código                | Função                                       |
            | -------------------------------| -------------------------------------------- |
            | plt.gca()                      | Obtém o gráfico (eixos) atual                |
            | .xaxis  /  .yaxis              | Seleciona o eixo X ou Y                      |
            | .set_major_locator()           | Define onde aparecem as marcações principais |
            | plt.MaxNLocator(integer=True)  | Força os ticks a serem números inteiros      |'''
        
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.tight_layout()  # Ajusta os espaçamentos entre gráficos 
    plt.show()          

def main():
    path = '/Users/manuelgallo/Documents/Universidade/2º ANO/TI/Projeto1/CarDataset.xlsx'

    data = pd.read_excel(path)

    matriz = data.values.tolist()

    varNames = data.columns.values.tolist()

    listaContador, alfabetos = conta_ocorrencias(matriz)

    print("\n=== MATRIZ ===")
    for linha in matriz:
        print("\n", linha)

    for i in range(len(listaContador)):
        print(f"\n=== Contagem de símbolos para {varNames[i]} ===")
        for valor, contagem in listaContador[i].items():
            print(f"{valor}: {contagem}")

    print("\n=== Alfabetos ===\n")
    for i in range(len(varNames)):
        print(f"\n{varNames[i]}")
        print("\n", alfabetos[i],"\n")

    grafico(data, varNames)

    return listaContador, alfabetos

listaContador, alfabetos = main()
