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
matriz = np.array(data.values.tolist(), dtype=np.uint16)
varNames = data.columns.values.tolist() #construir uma lista com os nomes das variaveis --1.c)

#imprimir a matriz --1.b)
for linha in matriz:
    print("\n", linha)


def contar_ocorrencias_numpy(matriz):
    """
    Conta as ocorrências de cada valor (0-65535) em cada variável (coluna)
    usando NumPy, de forma vetorizada e muito mais eficiente.
    Retorna uma lista de dicionários {valor: contagem}.
    """

    listaContador = []

    for i in range(len(varNames)):
        col = matriz[:, i]                       # extrai uma coluna
        valores, contagens = np.unique(col, return_counts=True)
        listaContador.append(dict(zip(valores, contagens)))

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

# Ajustar espaçamento entre os gráficos

listaContador = contar_ocorrencias_numpy(matriz)

for i, contador in enumerate(listaContador):
    print(f"\n--- Contagem de símbolos para {varNames[i]} ---")
    for valor, contagem in contador.items():
        print(f"{valor}: {contagem}")
        
plt.tight_layout()
plt.show()