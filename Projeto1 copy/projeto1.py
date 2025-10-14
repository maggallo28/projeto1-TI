import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Caminho do ficheiro
path = '/Users/manuelgallo/Documents/Universidade/2º ANO/TI/Projeto1/CarDataset.xlsx'
data = pd.read_excel(path)

# Converter para uint16 --3.a)
for i in data.columns:
    data[i] = data[i].astype(np.uint16)

# Converter para lista
matriz = data.values.tolist()
varNames = data.columns.values.tolist() #construir uma lista com os nomes das variaveis --1.c)

#imprimir a matriz --1.b)
for linha in matriz:
    print("\n", linha)

def contar_ocorrencias(matriz):
    """
    Função que calcula o número de ocorrências para cada símbolo do alfabeto
    (0 a 65535) para cada variável (coluna) da matriz.
    Retorna a lista de contadores e o tamanho do alfabeto.
    --ex.4
    """
    length = len(matriz) # quantidade de modelos de carro
    parametros = len(matriz[0]) # quantidade de parametros

    tamanho = 2**16 # estou a supor que o alfabeto vai de 0 a 2**16 - 1

    listaContador = []  #lista para cada variavel para poder armazenar a contagem de ocorrencias

    # criar uma sublista para cada coluna (e nao cada carro), com 2**16 zeros cada uma
    for i in range(parametros):
        #cria a sublista com tantos zeros como o tamanho, ou seja 2**16 zeros
        listaContador.append([0]*tamanho) #append serve para adicionar esta sublista à lista principal listaContador

    # contar as ocorrencias de cada valor
    for i in range(parametros): #percorre cada coluna(variavel)
        for j in range(length): #para cada variavel, percorre todos os carros
            valor = matriz[j][i] #vai buscar o valor do parâmetro i no carro j
            listaContador[i][valor] += 1 # adicionar 1 na posição do valor do parametro associado

    return listaContador, tamanho

listaContador, tamanho = contar_ocorrencias(matriz)

#imprimir os valores ( nao estou a perceber muito bem este ciclo)
for i in range(len(varNames)):
    print(f"\n--- Contagem de símbolos para {varNames[i]} ---")
    for j in range(tamanho):
        if listaContador[i][j] != 0:
            print(f"{j}:{listaContador[i][j]}") #nao estou a perceber como o codigo imprime o valor 

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

# Ajustar espaçamento entre os gráficos
plt.tight_layout()
plt.show()