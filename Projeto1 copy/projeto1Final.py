import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import huffmancodec as huffc

#-------------------------------Ex 2-----------------------------------
def conta_ocorrencias(matriz):

    matriz = matriz_uint16(matriz)
    
    listaContador = []
    simbolos = []

    for i in range(matriz.shape[1]):
        coluna = matriz[:, i]
        valores, contagemValor = np.unique(coluna, return_counts=True)
        listaContador.append(dict(zip(valores, contagemValor)))
        simbolos.append(valores)

    return listaContador, simbolos
#----------------------------------------------------------------------

#-------------------------------Ex 3.a---------------------------------
def matriz_uint16(matriz):
    matriz = np.array(matriz, dtype=np.uint16)
    return matriz
#----------------------------------------------------------------------

#-------------------------------Ex 2.a,b,c-----------------------------
def grafico(data, varNames):
    
    plt.subplots(3, 2, figsize=(10, 10))

    for i in range(len(varNames) - 1):
        plt.subplot(3, 2, i + 1)
        plt.scatter(data[varNames[i]], data['MPG'], c="#C50404")
        plt.title(f"MPG vs {varNames[i]}")
        plt.xlabel(varNames[i])
        plt.ylabel('MPG')

        # serve para aparecerem so inteiros no grafico
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # ajusta automaticamente os elementos do grafico (melhor visual)
    plt.tight_layout()
    plt.show()
#----------------------------------------------------------------------

#-------------------------------Ex 5-----------------------------------
def grafico_barras(varNames, listaContador):

    for i in range(len(listaContador)):
        lista_x_valor = list(listaContador[i].keys())
        lista_y_contagem = list(listaContador[i].values())

        valores_string = []
        for j in lista_x_valor:
            valores_string.append(str(j))

        plt.bar(valores_string, lista_y_contagem, color="#1f77b4")
        plt.title(f"Gráfico de Barras - {varNames[i]}")
        plt.xlabel(varNames[i])
        plt.ylabel('Count')
        plt.xticks(valores_string)

        # Mostra no máximo 12 valores no eixo X (para nao haver sobre posicao de valores no grafico)
        if len(valores_string) > 12:
            max_elementos = len(valores_string) // 12 
            plt.xticks(valores_string[::max_elementos])
        else:
            plt.xticks(valores_string)


        plt.tight_layout()
        plt.show()
#----------------------------------------------------------------------
        
#-------------------------------Ex 3.b---------------------------------
def alfabeto_uint16():
    tamanho = (2**16)
    lista_alafabeto = []
    for i in range(tamanho):
        lista_alafabeto.append(i)
    return lista_alafabeto
#----------------------------------------------------------------------
  
#-------------------------------Ex 6.a,b,c-----------------------------
def binning(data, coluna, bins):
    
    for minimo, maximo in bins:
        # Selecionar todos os valores do intervalo
        indices_intervalo = []
        for i in range(len(data[coluna])):
            if data.loc[i, coluna] >= minimo and data.loc[i, coluna] <= maximo:
                indices_intervalo.append(i)
        
        if indices_intervalo:

            valores = []
            for i in indices_intervalo:
                valores.append(data.loc[i, coluna])

            valor_mais_representativo = max(set(valores), key=valores.count)

            for i in indices_intervalo:
                data.loc[i, coluna] = valor_mais_representativo
    
    return data
#----------------------------------------------------------------------

#-------------------------------Ex 6.d,e-------------------------------
def binning_intervalos(matriz, varNames):

    matriz = matriz_uint16(matriz)

    bin_weight = []
    bin_disp = []
    bin_hp = []

    bin_var = [bin_weight, bin_disp, bin_hp]

    colunas_bin = ["Weight", "Displacement", "Horsepower"]

    for i in range(len(colunas_bin)):
        coluna_bin = []
        salto = 0
        contador = 0

        index = varNames.index(colunas_bin[i])

        for j in range(len(matriz)):
            coluna_bin.append(matriz[j][index])

        maximo = max(coluna_bin)

        if(i == 0):
            salto = 40

            while (((contador + 1) * salto - 1) < maximo):
                bin_var[i].append((contador * salto, (contador + 1) * salto - 1))
                contador += 1
        else:
            salto = 5

            while (((contador + 1) * salto - 1) < maximo):
                bin_var[i].append((contador * salto, (contador + 1) * salto - 1))
                contador += 1

    return bin_var[0], bin_var[1], bin_var[2]
#----------------------------------------------------------------------

#---------------------------------Ex 7---------------------------------
def media_bits(listaContador, matriz):

    entropias_vars = []
    for contador in listaContador:
        total = sum(contador.values())
        probs = []
        for v in contador.values():
            probs.append(v / total)

        entropia_variavel = -np.sum(probs * np.log2(probs))     #formula entropia
        entropias_vars.append(entropia_variavel)

    todos_valores = []
    for i in matriz:
        for j in i:
            todos_valores.append(j)

    valores, contagens = np.unique(todos_valores, return_counts=True)
    prob_total = contagens / np.sum(contagens)
    entropia_total = -np.sum(prob_total * np.log2(prob_total))        #formula entropia

    return entropias_vars, entropia_total
#----------------------------------------------------------------------

#---------------------------------Ex 8---------------------------------
def media_bits_huff(listaContador, simbolos):
    medias = []

    for i in range(len(listaContador)):
        contagens = np.array(list(listaContador[i].values()))
        total = np.sum(contagens)
        prob = contagens / total  

        var = []
        for simbolo, contagem in listaContador[i].items():
            var += [simbolo] * contagem

        codec = huffc.HuffmanCodec.from_data(var)
        s, lengths = codec.get_code_len()

        conta_media = np.sum(np.array(lengths) * prob)
        medias.append(conta_media)

        print(f"Variável {i + 1} : {conta_media:.2f} bits/símbolo")

    return medias
#----------------------------------------------------------------------

#-----------------------------------Main-------------------------------
def main():

    #-------------------------------Ex 1-------------------------------
    data = pd.read_excel('Projeto1 copy/CarDataset.xlsx')

    matriz = data.values.tolist()
    varNames = data.columns.values.tolist()
    #------------------------------------------------------------------

    #-------------------------------Ex 2.d-----------------------------
    grafico(data, varNames)
    listaContador, simbolos = conta_ocorrencias(matriz)
    grafico_barras(varNames, listaContador)
    #------------------------------------------------------------------

    #------------------------------Ex 7.a,b------------------------------
    entropias_vars, entropia_total = media_bits(listaContador, matriz)
    #------------------------------------------------------------------

    #-------------------------------Ex 6.a,b,c,d,e---------------------
    bin_weight = []
    bin_disp   = []
    bin_hp     = []

    bin_weight, bin_disp, bin_hp = binning_intervalos(matriz, varNames)

    data = binning(data, "Weight", bin_weight)
    data = binning(data, "Displacement", bin_disp)
    data = binning(data, "Horsepower", bin_hp)

    grafico(data, varNames)

    colunas_bin = ["Weight", "Displacement", "Horsepower"]
    matriz_bin = data[colunas_bin].values.tolist()
    listaContador_bin, _ = conta_ocorrencias(matriz_bin)

    grafico_barras(colunas_bin, listaContador_bin)
    #------------------------------------------------------------------

    #-------------------------------Ex 8-------------------------------
    medias = media_bits_huff(listaContador, simbolos)
    
    todos_simbolos = []
    for i in range(len(listaContador)):
        for simbolo, contagem in listaContador[i].items():
            todos_simbolos += [simbolo] * contagem

    codec_total = huffc.HuffmanCodec.from_data(todos_simbolos)
    symbols_total, lengths_total = codec_total.get_code_len()

    todos_simbolos = []
    for i in range(len(listaContador)):
        for simbolo, contagem in listaContador[i].items():
            todos_simbolos += [simbolo] * contagem

    codec_total = huffc.HuffmanCodec.from_data(todos_simbolos)
    symbols_total, lengths_total = codec_total.get_code_len()

    # probabilidades de todos os simbolos juntos
    valores, contagens = np.unique(todos_simbolos, return_counts=True)
    probs_total = contagens / np.sum(contagens)

    # comprimento médio do código em bits por símbolo.
    Lmedio_total = np.sum(np.array(lengths_total) * probs_total)

    print(f"\nConjunto completo : {Lmedio_total:.2f} bits/símbolo")

    #------------------------------------------------------------------
    return listaContador, simbolos

listaContador, simbolos =  main()