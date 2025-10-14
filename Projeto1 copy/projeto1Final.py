import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Caminho do ficheiro
path = '/Users/manuelgallo/Documents/Universidade/2º ANO/TI/Projeto1/CarDataset.xlsx'
data = pd.read_excel(path)

matriz = data.values.tolist()
varNames = data.columns.values.tolist()

def conta_ocorrencias(matriz):
    matriz = np.array(matriz, dtype=np.uint16)
    alfabeto = np.unique(matriz)
    listaContador = []
    
    for i in range(matriz.shape[1]):
        coluna = matriz[:, i]
        valores, contagens = np.unique(coluna, return_counts=True)
        contagem_coluna = np.zeros(len(alfabeto), dtype=int)
        indices = np.searchsorted(alfabeto, valores)
        contagem_coluna[indices] = contagens
        listaContador.append(dict(zip(alfabeto, contagem_coluna)))

    return listaContador, alfabeto

#mostrar figura --exercicio 2
fig, axs = plt.subplots(3, 2, figsize=(10, 10))  # (linhas, colunas) graficos na mesma figura --2.b)

for i in range(len(varNames) - 1):
    plt.subplot(3, 2, i + 1)  # (linhas, colunas, índice). graficos na mesma figura --2.b
    plt.scatter(data[varNames[i]], data['MPG'], c="#C50404")
    plt.title(f"MPG vs {varNames[i]}")  #titulo --2.c)
    plt.xlabel(varNames[i]) #nome da variavel correspondente --2.c)
    plt.ylabel('MPG')       #nome da variavel correspondente --2.c)
    
    # Garantir que os ticks sejam inteiros --dados discretos --2.a)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

listaContador = conta_ocorrencias(matriz)

#Imprime o reultado
for i in range(len(listaContador)):
    print("\n_____Contagem de símbolos para",varNames[i], "_____")

    posicao = listaContador[i]

    for numero in posicao:
        print(numero, ":", posicao[numero])

# Ajustar espaçamento entre os gráficos
plt.tight_layout()
plt.show()