import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import huffmancodec as huffc


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

#-------------------------------Ex 3.a---------------------------------
def matriz_uint16(matriz):
    matriz = np.array(matriz, dtype=np.uint16)
    return matriz
#----------------------------------------------------------------------

#-------------------------------Ex 3.b---------------------------------
def alfabeto_uint16():
    return np.arange(2**16, dtype=np.uint16)
#----------------------------------------------------------------------

#-------------------------------Ex 4-----------------------------------
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

#-------------------------------Ex 5-----------------------------------
def grafico_barras(varNames, listaContador):

    for i in range(len(listaContador)):
        lista_x_valor = list(listaContador[i].keys())
        lista_y_contagem = list(listaContador[i].values())

        valores_string = []
        for j in lista_x_valor:
            valores_string.append(str(j))

        plt.bar(valores_string, lista_y_contagem, color="#C50404")
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
def media_bits_huff(listaContador, varNames):
    for i in range(len(listaContador)):
        contagens = np.array(list(listaContador[i].values()))
        total = np.sum(contagens)
        prob = contagens / total  

        var = []
        for simbolo, contagem in listaContador[i].items():
            var += [simbolo] * contagem

        codec = huffc.HuffmanCodec.from_data(var)
        s, lengths = codec.get_code_len()

        media = np.sum(np.array(lengths) * prob)
        variancia = np.sum(prob * (np.array(lengths) - media)**2) 

        print(f"{varNames[i]} : {media:.5f} bits/simbolo | Variancia: {variancia:.5}") 
#----------------------------------------------------------------------

#---------------------------------Ex 9---------------------------------
def correlacao_pearson(data, varNames):
    
    mpg = data['MPG'].values

    for i in varNames:
        if i != 'MPG':
            dados_coluna = data[i].values
            # cc de pearson esta na posicao [0, 1] (da matriz obtida pela funcao corrcoef) --> [[1 , r],[r , 1]]
            r = np.corrcoef(mpg, dados_coluna)[0, 1]
            print(f"MPG e {i} : {r:.5f}")
#----------------------------------------------------------------------

#---------------------------------Ex 10--------------------------------
def mi(data, varNames, listaContador):
    
    cnt_y = np.array(list(listaContador[6].values()))
    py = cnt_y / np.sum(cnt_y)
    hy = -np.sum(py * np.log2(py))

    for i in range(len(varNames)-1):
        
        cnt_x = np.array(list(listaContador[i].values()))
        px = cnt_x / np.sum(cnt_x)
        hx = -np.sum(px * np.log2(px))

        coluna = data[varNames[i]].values
        pares = np.array(list(zip(coluna, data[varNames[6]].values)))
        _, cnt_xy = np.unique(pares, axis=0, return_counts=True)
        pxy = cnt_xy / np.sum(cnt_xy)
        hxy = -np.sum(pxy * np.log2(pxy))

        mi = hx + hy - hxy

        print(f"{varNames[i]} : {mi:.5f} bits")
#----------------------------------------------------------------------

#---------------------------------Ex 11--------------------------------
def estimacao_MPG(matriz):
    
    matriz = np.array(matriz)
    media_acceleracao = np.mean(matriz[:,0])
    media_weight = np.mean(matriz[:,5])

    for n in range(3):
        col = ["Normal","Acceleration","Weight"]
        antigo_mpg = []
        novo_mpg = []

        for i in range(len(matriz)):
            if(n==0):
                xx = matriz[i][0]
                yy = matriz[i][5]
            elif(n==1):
                xx = media_acceleracao
                yy = matriz[i][5]
            elif(n==2):
                xx = matriz[i][0]
                yy = media_weight
            var_novo_mpg = -5.5241 -0.146*xx -0.4909*matriz[i][1] +0.0026*matriz[i][2] -0.0045*matriz[i][3] +0.6725*matriz[i][4] -0.0059*yy
            novo_mpg.append(var_novo_mpg)
            antigo_mpg.append(matriz[i][6])
        
        mpg_real = np.array(antigo_mpg)
        mpg_estimado = np.array(novo_mpg)

        rms_error = np.sqrt(np.mean((mpg_real - mpg_estimado)**2))
        mae = np.mean(np.abs(mpg_real - mpg_estimado))
        #for j in range(len(mpg_estimado)):
        #    print(f"Est : {mpg_estimado[j]:.2f} | Real : {mpg_real[j]:.2f}")

        print(f"{col[n]} : ")
        print(f"root mean square error : {rms_error:.5}")
        print(f"mean absolut error : {mae:.5}")
#----------------------------------------------------------------------

#-----------------------------------Main-------------------------------
def main():

    #-------------------------------Ex 1-------------------------------
    data = pd.read_excel('Projeto1 copy/CarDataset.xlsx')

    matriz = data.values.tolist()
    varNames = data.columns.values.tolist()
    #------------------------------------------------------------------

    #-------------------------------Ex 11------------------------------
    print("\nex11-------------------------------------------")
    estimacao_MPG(matriz)
    print("-----------------------------------------------")
    #------------------------------------------------------------------

    #-------------------------------Ex 2.d-----------------------------
    grafico(data, varNames)
    listaContador, simbolos = conta_ocorrencias(matriz)
    grafico_barras(varNames, listaContador)
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

    #------------------------------Ex 7.a,b----------------------------
    listaContador[2] = listaContador_bin[1]  
    listaContador[3] = listaContador_bin[2]  
    listaContador[5] = listaContador_bin[0]  
    print("\nex7--------------------------------------------")
    media_bits(listaContador, matriz, varNames)
    print("-----------------------------------------------")
    #------------------------------------------------------------------

    #-------------------------------Ex 8-------------------------------
    print("\nex8--------------------------------------------")
    print("Medias e Variancas : ")
    media_bits_huff(listaContador, varNames)
    print("-----------------------------------------------")
    #------------------------------------------------------------------

    #-------------------------------Ex 10------------------------------
    print("\nex10-------------------------------------------")
    print("Informacao Mutua MPG e :")
    mi(data, varNames, listaContador)
    print("-----------------------------------------------")
    #------------------------------------------------------------------

    #-------------------------------Ex 9-------------------------------
    print("\nex9--------------------------------------------")
    print("Coeficientes de correlacao de pearson com MPG : ")
    correlacao_pearson(data, varNames)
    print("-----------------------------------------------")
    #------------------------------------------------------------------

    return listaContador, simbolos

listaContador, simbolos =  main()