import numpy as np


# Aqui obtemos a base de treino, onde a proporção escolhida foi de 70%.
def retorna_treino(base):
    treino = base.sample(frac=0.7)
    return treino

# A base de teste é obtida retirando a base de treino do Dataframe.
def retorna_teste(base, base_treino):
    teste = base.drop(base_treino.index)
    return teste


# Nesta função, calculamos a sensibilidade, confiabilidades,
# dentre outros a partir da matriz de confusão.
def calcula_resultados(matriz, verbose=False):
    
    num_classes = len(matriz)

    sensibilidade = np.zeros([num_classes])
    especificidade = np.zeros([num_classes])
    confiabilidade_positiva = np.zeros([num_classes])
    confiabilidade_negativa = np.zeros([num_classes])

    tp = np.zeros([num_classes])
    tn = np.zeros([num_classes])
    fn = np.zeros([num_classes])
    fp = np.zeros([num_classes])

    acertos = 0
    acuracia = 0
    total = 0

    for classe in range(num_classes):
        for linha in range(num_classes):
            for coluna in range(num_classes):
                if classe == linha == coluna:
                    tp[classe] += matriz[linha][coluna]
                elif classe != linha == coluna:
                    tn[classe] += matriz[linha][coluna]
                elif classe == linha != coluna:
                    fn[classe] += matriz[linha][coluna]
                elif classe == coluna != linha:
                    fp[classe] += matriz[linha][coluna]

    if verbose:
        print('TP =', tp)
        print('TN =', tn)
        print('FN =', fn)
        print('FP =', fp)

    for linha in range(num_classes):
        for coluna in range(num_classes):
            if linha == coluna:
                acertos += matriz[linha][coluna]
            total += matriz[linha][coluna]

    acuracia = (acertos*100)/total

    for classe in range(num_classes):
        sensibilidade[classe] = tp[classe]/(tp[classe] + fn[classe])
        especificidade[classe] = tn[classe]/(tn[classe] + fp[classe])
        confiabilidade_positiva[classe] = tp[classe]/(tp[classe] + fp[classe])
        confiabilidade_negativa[classe] = tn[classe]/(tn[classe] + fn[classe])
        
        if tp[classe] + fn[classe] == 0:
            sensibilidade[classe] = 0
        if tn[classe] + fp[classe] == 0:
            especificidade[classe] = 0
        if tp[classe] + fp[classe] == 0:
            confiabilidade_positiva[classe] = 0
        if tn[classe] + fn[classe] == 0:
            confiabilidade_negativa[classe] = 0

    # Se quisermos ver todos os detalhes da execução, podemos escolher este
    # atributo verbose como True.
        if verbose:
            print('----------- Classe %d -----------' %(classe+1))
            print('Sensibilidade: ', sensibilidade[classe])
            print('Especificidade: ', especificidade[classe])
            print('Confiabilidade Positiva: ', confiabilidade_positiva[classe])
            print('Confiabilidade Negativa: ', confiabilidade_negativa[classe])
    if verbose:
        print('Media da Sensibilidade: ', np.mean(sensibilidade))
        print('Media da Especificidade: ', np.mean(especificidade))
        print('Media da Confiabilidade Positiva: ', np.mean(confiabilidade_positiva))
        print('Media da Confiabilidade Negativa: ', np.mean(confiabilidade_negativa))

    if verbose:
        print('Acurácia:', acuracia, end='\n')

    # Por fim, retornamos a acurácia da execução.
    return acuracia
