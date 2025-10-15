import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def conta_ocorrencias(matriz):
    matriz = np.array(matriz, dtype=np.uint16)
    listaContador = []
    alfabetos = []

    for i in range(matriz.shape[1]):
        coluna = matriz[:, i]
        valores, contagemValor = np.unique(coluna, return_counts=True)
        listaContador.append(dict(zip(valores, contagemValor)))
        alfabetos.append(valores)

    return listaContador, alfabetos

def grafico(data, varNames):
    plt.subplots(3, 2, figsize=(10, 10))

    for i in range(len(varNames) - 1):
        plt.subplot(3, 2, i + 1)
        plt.scatter(data[varNames[i]], data['MPG'], c="#C50465")
        plt.title(f"MPG vs {varNames[i]}")
        plt.xlabel(varNames[i])
        plt.ylabel('MPG')
        
        # serve para aparecerem so inteiros no grafico
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # ajusta automaticamente os elementos do grafico (melhor visual)
    plt.tight_layout()
    plt.show()

def grafico_barras(varNames, listaContador):
    plt.subplots(3, 2, figsize=(10, 10))

    for i in range(len(varNames)):

        #for c,v in listaContador(c,v):

        
        
        plt.xlabel(varNames[i])
        plt.ylabel('Count')
        
        # serve para aparecerem so inteiros no grafico
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))






def main():
    path = '/Users/manuelgallo/Documents/Universidade/2º ANO/TI/Projeto1/CarDataset.xlsx'
    data = pd.read_excel(path)

    matriz = data.values.tolist()
    varNames = data.columns.values.tolist()

    grafico(data, varNames)
    grafico_barras(varNames, listaContador)

    listaContador, alfabeto = conta_ocorrencias(matriz)

    return listaContador, alfabeto

listaContador, alfabeto = main()