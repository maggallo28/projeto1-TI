import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Caminho do ficheiro
path = '/Users/manuelgallo/Documents/Universidade/2º ANO/TI/Projeto1/CarDataset.xlsx'
data = pd.read_excel(path)

# Converter para lista
matriz = data.values.tolist()
varNames = data.columns.values.tolist() #construir uma lista com os nomes das variaveis --1.c)

#imprimir a matriz --1.b)
for linha in matriz:
    print("\n", linha)

#funcao para contar o numero de ocorencias de cada valor do alfabeto
def conta_occorencias(matriz):
    
    #transforma os elementos da matriz (uint8) em uint16
    matriz = np.array(matriz, dtype=np.uint16   )# Converter para uint16 --3.a)

    listaContador = []

    #conta para cada valor presente na matriz o numero de ocorencias deste
    for i in range(matriz.shape[1]):  #percorre cada coluna
        coluna = matriz[:, i] #pega todos os elementos da coluna (i)
        contador = {}

        for valor in coluna:

            #adiciona +1 ou inicializa o a 1 se ele nao exitir ainda
            if valor in contador:
                contador[valor] += 1
            else:
                contador[valor] = 1

        #adiciona esses valores a nova lista 
        listaContador.append(contador)

    return listaContador

#mostrar figura --exercicio 2
fig, axs = plt.subplots(3, 2, figsize=(10, 10))  # (linhas, colunas) graficos na mesma figura --2.b)

for i in range(len(varNames) - 1):
    plt.subplot(3, 2, i + 1)  # (linhas, colunas, índice). graficos na mesma figura --2.b
    plt.scatter(data[varNames[i]], data['MPG'])
    plt.title(f"MPG vs {varNames[i]}")  #titulo --2.c)
    plt.xlabel(varNames[i]) #nome da variavel correspondente --2.c)
    plt.ylabel('MPG')       #nome da variavel correspondente --2.c)
    
    # Garantir que os ticks sejam inteiros --dados discretos --2.a)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

listaContador = conta_occorencias(matriz)

#Imprime o reultado
for i in range(len(listaContador)):
    print("\n_____Contagem de símbolos para",varNames[i], "_____")

    posicao = listaContador[i]

    for numero in posicao:
        print(numero, ":", posicao[numero])

# Ajustar espaçamento entre os gráficos
plt.tight_layout()
plt.show()