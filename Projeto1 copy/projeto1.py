import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def conta_ocorrencias(matriz):
    matriz = np.array(matriz, dtype=object)
    listaContador = []
    alfabetos = []

    for i in range(matriz.shape[1]):
        coluna = matriz[:, i]
        valores, contagens = np.unique(coluna, return_counts=True)
        listaContador.append(dict(zip(valores, contagens)))
        alfabetos.append(valores)

    return listaContador, alfabetos


def plot_mpg_scatter(data, varNames):
    plt.close('all')  
    fig = plt.subplots(3, 2, figsize=(10, 10))

    for i in range(len(varNames) - 1):
        plt.subplot(3, 2, i + 1)
        plt.scatter(data[varNames[i]], data['MPG'], c="#C50404")
        plt.title(f"MPG vs {varNames[i]}")
        plt.xlabel(varNames[i])
        plt.ylabel('MPG')
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.tight_layout()
    plt.show()


def main():
    path = '/Users/manuelgallo/Documents/Universidade/2º ANO/TI/Projeto1/CarDataset.xlsx'
    data = pd.read_excel(path)

    matriz = data.values.tolist()
    varNames = data.columns.values.tolist()

    plot_mpg_scatter(data, varNames)

    listaContador, alfabetos = conta_ocorrencias(matriz)

    # === Impressão da matriz ===
    print("\n===== MATRIZ DE DADOS =====")
    for linha in matriz:
        print(linha)

    # === Impressão das ocorrências ===
    for i in range(len(listaContador)):
        print(f"\n_____ Contagem de símbolos para {varNames[i]} _____")
        for valor, contagem in listaContador[i].items():
            print(f"{valor}: {contagem}")

    return listaContador, alfabetos


listaContador, alfabetos = main()
