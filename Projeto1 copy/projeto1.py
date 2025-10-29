import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import huffmancodec as huffc

#-------------------------------Ex 2-----------------------------------
def conta_ocorrencias(matriz):

    matriz = matriz_uint16(matriz)     #garante que matriz fica em uint16
    
    listaContador = []     #lista para guardar um dicionario por variavel com contagens
    simbolos = []          #lista para guardar os simbolos (valores unicos) de cada variavel

    for i in range(matriz.shape[1]):       #percorrer cada coluna da matriz
        coluna = matriz[:, i]              #selecionar a coluna i
        valores, contagemValor = np.unique(coluna, return_counts=True)  #conta ocorrencias
        listaContador.append(dict(zip(valores, contagemValor)))        #cria dicionario {valor: contagem}
        simbolos.append(valores)                                       #guarda os valores unicos

    return listaContador, simbolos
#----------------------------------------------------------------------

#-------------------------------Ex 3.a---------------------------------
def matriz_uint16(matriz):
    matriz = np.array(matriz, dtype=np.uint16)     #converte os valores para uint16
    return matriz
#----------------------------------------------------------------------

#-------------------------------Ex 2.a,b,c-----------------------------
def grafico(data, varNames):
    
    plt.subplots(3, 2, figsize=(10, 10))      #figura com grelha 3x2

    for i in range(len(varNames) - 1):        #percorre todas variaveis exceto MPG
        plt.subplot(3, 2, i + 1)              #define o subplot
        plt.scatter(data[varNames[i]], data['MPG'], c="#C50404")   #grafico de dispersao
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

    for i in range(len(listaContador)):       #para cada variavel
        lista_x_valor = list(listaContador[i].keys())     #valores unicos
        lista_y_contagem = list(listaContador[i].values()) #contagens

        valores_string = []      #converter valores para string para colocar no eixo X
        for j in lista_x_valor:
            valores_string.append(str(j))

        plt.bar(valores_string, lista_y_contagem, color="#1f77b4")  #grafico de barras
        plt.title(f"Gráfico de Barras - {varNames[i]}")
        plt.xlabel(varNames[i])
        plt.ylabel('Count')
        plt.xticks(valores_string)

        # Mostra no máximo 12 valores no eixo X (evita sobreposicoes)
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
    tamanho = (2**16)     #65536 simbolos possiveis em uint16
    lista_alafabeto = []
    for i in range(tamanho):
        lista_alafabeto.append(i)
    return lista_alafabeto
#----------------------------------------------------------------------
  
#-------------------------------Ex 6.a,b,c-----------------------------
def binning(data, coluna, bins):
    
    for minimo, maximo in bins:     #para cada intervalo
        indices_intervalo = []       #guardar indices das linhas dentro do intervalo
        for i in range(len(data[coluna])):
            if data.loc[i, coluna] >= minimo and data.loc[i, coluna] <= maximo:
                indices_intervalo.append(i)
        
        if indices_intervalo:       #se houver valores no intervalo
            valores = []
            for i in indices_intervalo:
                valores.append(data.loc[i, coluna])   #recolhe valores do intervalo

            valor_mais_representativo = max(set(valores), key=valores.count)  #valor mais frequente

            for i in indices_intervalo:
                data.loc[i, coluna] = valor_mais_representativo  #substitui valores pelo mais freq
    
    return data
#----------------------------------------------------------------------

#-------------------------------Ex 6.d,e-------------------------------
def binning_intervalos(matriz, varNames):

    matriz = matriz_uint16(matriz)      #garante tipo uint16

    bin_weight = []    #intervalos para Weight
    bin_disp = []      #intervalos para Displacement
    bin_hp = []        #intervalos para Horsepower

    bin_var = [bin_weight, bin_disp, bin_hp]

    colunas_bin = ["Weight", "Displacement", "Horsepower"]

    for i in range(len(colunas_bin)):        #para cada uma das 3 variaveis
        coluna_bin = []                      #guardar valores da coluna
        salto = 0                            #tamanho do intervalo
        contador = 0

        index = varNames.index(colunas_bin[i])   #indice da coluna

        for j in range(len(matriz)):
            coluna_bin.append(matriz[j][index])   #extrai valores dessa coluna

        maximo = max(coluna_bin)  #valor max para saber ate onde criar bins

        if(i == 0):               #se for Weight
            salto = 40            #tamanho do bin
            while (((contador + 1) * salto - 1) < maximo):
                bin_var[i].append((contador * salto, (contador + 1) * salto - 1))
                contador += 1
        else:                     #para disp e hp
            salto = 5
            while (((contador + 1) * salto - 1) < maximo):
                bin_var[i].append((contador * salto, (contador + 1) * salto - 1))
                contador += 1

    return bin_var[0], bin_var[1], bin_var[2]
#----------------------------------------------------------------------

#---------------------------------Ex 7---------------------------------
def media_bits(listaContador, matriz):

    entropias_vars = []     #guardar a entropia de cada variavel
    for contador in listaContador:      #contador é um dicionario de listacontador, para cada contador em lista_contador
        total = sum(contador.values())      #somar todas as ocorrencias -> numero de amostars dessa avriavel
        probs = []                          #lista vazia para guardar os valores de probs
        for v in contador.values():     #para cada contagem em contador
            probs.append(v / total)     #contagem/total

        entropia_variavel = -np.sum(probs * np.log2(probs))     #formula entropia
        entropias_vars.append(entropia_variavel)

    todos_valores = []          #lista vazia com todos os valores da matriz
    for linha in matriz:        #para cada linha
        for j in linha:         #para cada valor
            todos_valores.append(j) #adiciona valor

    valores, contagens = np.unique(todos_valores, return_counts=True)       #contar quantas vezes se repete um valor
    prob_total = contagens / np.sum(contagens)              #ver essas contagens e dividir pelo total
    entropia_total = -np.sum(prob_total * np.log2(prob_total))        #formula entropia

    return entropias_vars, entropia_total
#----------------------------------------------------------------------

#---------------------------------Ex 8---------------------------------
def media_bits_huff(listaContador, simbolos):
    """
    Para cada variável:
    - reconstrói a lista de símbolos repetidos (cada símbolo repetido 'contagem' vezes)
      porque HuffmanCodec.from_data espera uma sequência de símbolos (dados brutos).
    - cria o codec de Huffman
    - obtém comprimentos de código (bits) por símbolo com codec.get_code_len()
    - calcula o comprimento médio: soma(lengths * prob)

    Retorna: lista com o comprimento médio para cada variável.
    """
    medias = []

    for i in range(len(listaContador)):
        # extrair contagens e converter para probabilidades
        contagens = np.array(list(listaContador[i].values()))
        total = np.sum(contagens)
        prob = contagens / total

        # reconstruir a sequência de símbolos repeteidos conforme as contagens
        # ex.: {4:3, 6:2} -> [4,4,4,6,6]
        var = []
        for simbolo, contagem in listaContador[i].items():
            var += [simbolo] * contagem

        # construir tabela de Huffman a partir dos dados
        codec = huffc.HuffmanCodec.from_data(var)
        s, lengths = codec.get_code_len()  # s: símbolos, lengths: comprimentos dos códigos

        # comprimento médio (esperança dos comprimentos com as probabilidades)
        conta_media = np.sum(np.array(lengths) * prob)
        medias.append(conta_media)

        print(f"Variável {i + 1} : {conta_media:.2f} bits/símbolo")

    return medias
#----------------------------------------------------------------------

#-----------------------------------Main-------------------------------
def main():

    #-------------------------------Ex 1-------------------------------
    data = pd.read_excel('Projeto1 copy/CarDataset.xlsx')

    matriz = data.values.tolist()                 #matriz como lista de listas (linhas)
    varNames = data.columns.values.tolist()       #nomes das variaveis/colunas
    #------------------------------------------------------------------

    #-------------------------------Ex 2.d-----------------------------
    grafico(data, varNames)
    listaContador, simbolos = conta_ocorrencias(matriz)
    grafico_barras(varNames, listaContador)
    #------------------------------------------------------------------

    #------------------------------Ex 7.a,b------------------------------
    entropias_vars, entropia_total = media_bits(listaContador, matriz)
    # entropias_vars -> lista com entropia de cada variavel
    # entropia_total -> entropia global do conjunto (todos os valores juntos)
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
    
    # Construir uma sequência completa com todos os símbolos (cada símbolo repetido segundo sua contagem)
    # para gerar um codec global e medir o comprimento médio do código para o conjunto todo.
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