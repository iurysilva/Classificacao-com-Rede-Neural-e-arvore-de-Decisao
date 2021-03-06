import numpy as np
import pandas as pd
from estrutura_da_rede_neural import Camada
from estrutura_da_rede_neural.funcoes_uteis import sigmoide
from estrutura_da_rede_neural.funcoes_uteis import multiplicar_matrizes
from estrutura_da_rede_neural.funcoes_uteis import derivar_sigmoide
from estrutura_da_rede_neural.funcoes_uteis import tahn
from bancos_de_dados.ferramentas import *


# O Objeto Rede Neural, onde ficarão armazenadas as camadas, especificações do
# banco de dados como número de atributos de entrada e saída, o próprio banco
# para utilização pode parte dela, e outros parâmetros de execução e informações
# importantes como a linha atual que a rede está lendo do banco, o valor esperado
# para a classe dessa linha entre outros.
class Rede_Neural:
    def __init__(self, atributos_entradas, atributos_saidas,  num_camadas, neuronios_por_camada_oculta, banco):
        self.atributos_de_entrada = atributos_entradas
        self.atributos_de_saida = atributos_saidas
        self.banco = banco
        self.num_entradas = self.atributos_de_entrada.size
        self.num_saidas = self.atributos_de_saida.size
        self.numero_camadas = num_camadas
        self.neuronios_por_camada_oculta = neuronios_por_camada_oculta
        self.camadas = self.cria_camadas()
        self.valor_esperado = None
        self.learning_rate = 1
        self.linha_atual = None

    # Este método em essência serve para verificar se as camadas foram criadas de
    # forma correta, ele mostra na tela várias informações referentes a todas as
    # camadas da rede neural.
    def mostra_informacoes_das_camadas(self):
        print('')
        for camada in range(self.numero_camadas):
            print("Informações da camada %d: " % camada)
            print("Numero de neuronios: ", self.camadas[camada].numero_neuronios)
            print("Camada final?: ", self.camadas[camada].final)
            print("Sinapses da camada: ")
            print(self.camadas[camada].sinapses, "\n")

    # Este método é chamado no momento de criação da rede neural, ao mesmo tempo
    # ele irá criar as camadas conforme a arquitetura definida no arquivo de
    # execução do algoritmo.
    def cria_camadas(self):
        camadas = []
        for camada in range(self.numero_camadas):
            if camada == 0:
                camadas.append(Camada(self.num_entradas))
            elif camada == self.numero_camadas-1:
                camadas.append(Camada(self.num_saidas))
            else:
                camadas.append(Camada(self.neuronios_por_camada_oculta))
        camadas[-1].final = True
        return camadas

    # Este método deve ser chamado imediatamente após a criação da rede, ele irá
    # inserir todas as sinapses entre todos os neurônios de todas as camadas, além
    # disso, ele irá inserir o vetor de bias que será utilizado no Feedfoward e
    # Backpropagation, as sinapses (pesos) são criados de forma aleatória, com
    # valores entre 0 e 1 para cada peso.
    def insere_sinapses_e_bias(self):
        for camada in range(self.numero_camadas):
            if not self.camadas[camada].final:
                camada_1 = self.camadas[camada]
                camada_2 = self.camadas[camada+1]
                linhas = camada_2.numero_neuronios
                colunas = camada_1.numero_neuronios
                sinapses = np.random.rand(linhas, colunas)
                self.camadas[camada].sinapses = np.copy(sinapses)
                self.camadas[camada].bias = np.zeros((self.camadas[camada + 1].numero_neuronios, 1))

    # Este método é responsável por inserir os atributos da linha que será lida na
    # primeira camada, por isso seu único parâmetro é a linha do banco que será lida.
    def inserir_entradas(self, linha):
        banco = self.banco.values
        for entrada in range(self.num_entradas):
            atributo = self.atributos_de_entrada[entrada]
            self.camadas[0].neuronios[entrada] = sigmoide(banco[linha][atributo])

    # Este método definirá qual será o valor esperado, ou seja, o valor correto da
    # classe que possui os atributos na camada de entrada, note que este valor
    # já foi convertido para seu equivalente na função Sigmoide.
    def inserir_saidas(self, linha):
        banco = self.banco.values
        for saida in range(self.num_saidas):
            atributo = self.atributos_de_saida[saida]
            valor = banco[linha][atributo]
            # print(valor)
            if valor == 'Iris-setosa':
                valor = 1
            elif valor == 'Iris-versicolor':
                valor = 2
            elif valor == 'Iris-virginica':
                valor = 3
            else:
                valor = valor
            self.valor_esperado = sigmoide(valor)

    # O método feedfoward fará os calculos necessários utilizando os valores na
    # camada de entrada para que se chegue ao valor de saída da rede, armazenado
    # na última camada.
    def feedfoward(self):
        # print("lendo linha: ", self.linha_atual)
        for camada_atual in range(self.numero_camadas-1):
            camada = self.camadas[camada_atual]
            if not camada.final:
                multiplicacao_matricial = multiplicar_matrizes(camada.sinapses, camada.neuronios)
                multiplicacao_matricial = multiplicacao_matricial + camada.bias
                self.camadas[camada_atual + 1].neuronios = sigmoide(multiplicacao_matricial)
                '''print('sinapses ligadas a camada %d: ' % camada_atual)
                print(camada.sinapses)
                print('neuronios da camada atual: ')
                print(camada.neuronios)
                print('multiplicação das sinapses pelos neuronios: ')
                print(self.camadas[camada_atual+1].neuronios)'''
        # print("valor na camada final: ", self.camadas[-1].neuronios)
        # print("valor esperado: ", self.valor_esperado, "\n")

    # O método a seguir serve para testar o feedfoward uma única ves em uma linha
    # do bando de dados, isso é importante para que possamos fazer verificações
    # únicas no bando depois que a rede já aprendeu, ou caso queiramos executar
    # o feedfoward várias vezes já inserindo as entradas e saídas podemos chamar
    # essa função em loop.
    def testar_feed_foward(self, linha, banco):
        self.banco = banco
        self.inserir_entradas(linha)
        self.inserir_saidas(linha)
        self.linha_atual = linha
        self.feedfoward()

    # Função para propagar o erro obtido na saída da rede neural, modificando os
    # pesos das sinapses entre as camadas, além de modificar o Bias
    def backpropagation(self):
        erro_saida = self.valor_esperado - self.camadas[-1].neuronios
        derivada_saida = derivar_sigmoide(self.camadas[-1].neuronios)
        transposta_oculto = np.transpose(self.camadas[-2].neuronios)

        gradiente = np.multiply(derivada_saida, erro_saida)
        gradiente = gradiente * self.learning_rate

        self.camadas[-2].bias = self.camadas[-2].bias + gradiente

        delta_pesos_oculto_saida = np.matmul(gradiente, transposta_oculto)
        self.camadas[-2].sinapses = self.camadas[-2].sinapses + delta_pesos_oculto_saida
        self.camadas[-1].erro = erro_saida

        for i in range(self.numero_camadas - 2, 0, -1):
            transposta_pesos = np.transpose(self.camadas[i].sinapses)
            erro = np.matmul(transposta_pesos, self.camadas[i+1].erro)
            derivada = derivar_sigmoide(self.camadas[i].neuronios)
            transposta = np.transpose(self.camadas[i-1].neuronios)
    
            gradiente_O = np.multiply(erro, derivada)
            gradiente_O = gradiente_O * self.learning_rate
    
            self.camadas[i-1].bias = self.camadas[i-1].bias + gradiente_O
    
            delta_pesos = np.matmul(gradiente_O, transposta)
            self.camadas[i-1].sinapses = self.camadas[i-1].sinapses + delta_pesos
            self.camadas[i].erro = erro

    # Função para testar o algoritmo após o aprendizado, apenas classificando as
    # amostras sem modificar os seus parâmetros
    def aprender(self, num_epocas, base_treino):
        self.banco = base_treino
        num_linhas = len(base_treino)

        for epocas in range(num_epocas):

            for linha in range(num_linhas):
                self.linha_atual = linha
                self.inserir_entradas(linha)
                self.inserir_saidas(linha)
                self.feedfoward()
                self.backpropagation()

    # Função que executa o aprendizado do algoritmo utilizando a base de treino.
    # A mesma utiliza outras funções, como o backpropagation() e o feedfoward()
    def testar(self, tipos_saidas, base_teste):
        matriz_confusao = np.zeros((len(tipos_saidas), len(tipos_saidas)))
        num_linhas = len(base_teste)
        resultado = None
        base_numpy = base_teste.values

        for linha in range(num_linhas):
            self.testar_feed_foward(linha, base_teste)

            valor_1 = sigmoide(tipos_saidas[0])
            valor_2 = sigmoide(tipos_saidas[1])
            valor_ultimo = sigmoide(tipos_saidas[-1])
            valor_penultimo = sigmoide(tipos_saidas[-2])

            if len(tipos_saidas) == 2:

                if self.camadas[-1].neuronios[0][0] < ((valor_1 + valor_2) / 2):
                    resultado = np.where(tipos_saidas == tipos_saidas[0])

                elif self.camadas[-1].neuronios[0][0] >= ((valor_1 + valor_2) / 2):
                    resultado = np.where(tipos_saidas == tipos_saidas[-1])
            else:

                if self.camadas[-1].neuronios[0][0] < ((valor_1 + valor_2) / 2):
                    resultado = np.where(tipos_saidas == tipos_saidas[0])

                elif (valor_1 + valor_2) / 2 <= self.camadas[-1].neuronios[0][0] < ((valor_ultimo + valor_penultimo) / 2):

                    for j in range(1, len(tipos_saidas) - 1):

                        valor_1 = sigmoide(tipos_saidas[j])
                        valor_2 = sigmoide(tipos_saidas[j - 1])
                        valor_3 = sigmoide(tipos_saidas[j + 1])

                        if (self.camadas[-1].neuronios[0][0] >= (valor_1 + valor_2)/2) and (self.camadas[-1].neuronios[0][0] < (valor_1 + valor_3))/2:
                            resultado = np.where(tipos_saidas == tipos_saidas[j])

                elif self.camadas[-1].neuronios[0][0] >= ((valor_ultimo + valor_penultimo) / 2):
                    resultado = np.where(tipos_saidas == tipos_saidas[-1])

            valor_teste = np.where(tipos_saidas == base_numpy[linha][self.atributos_de_saida[0]])
            matriz_confusao[int(valor_teste[0])][int(resultado[0])] += 1

        print(matriz_confusao)

        return matriz_confusao


