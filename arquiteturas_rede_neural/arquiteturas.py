import numpy as np
from bancos_de_dados import bd_bandeiras
from bancos_de_dados import bd_iris
from bancos_de_dados import bd_vidros
from bancos_de_dados import bd_vinho
from estrutura_da_rede_neural import Rede_Neural


def criar_arquitetura_vidros():
    atributos_entrada = np.array([1, 2, 3, 4, 6, 7, 8, 9])
    atributos_saida = np.array([10])
    num_de_camadas = 4
    num_de_neuronios_por_camada_oculta = 8
    rede = Rede_Neural(atributos_entrada, atributos_saida, num_de_camadas, num_de_neuronios_por_camada_oculta,
                       bd_vidros)
    return rede


def criar_arquitetura_bandeiras():
    atributos_entrada = np.array([1, 4, 5, 6, 7])
    atributos_saida = np.array([2])
    num_de_camadas = 3
    num_de_neuronios_por_camada_oculta = 6
    rede = Rede_Neural(atributos_entrada, atributos_saida, num_de_camadas, num_de_neuronios_por_camada_oculta,
                       bd_bandeiras)
    return rede


def criar_arquitetura_iris():
    atributos_entrada = np.array([0, 1, 2, 3])
    atributos_saida = np.array([4])
    num_de_camadas = 4
    num_de_neuronios_por_camada_oculta = 6
    rede = Rede_Neural(atributos_entrada, atributos_saida, num_de_camadas, num_de_neuronios_por_camada_oculta,
                       bd_iris)
    return rede


def criar_arquitetura_vinho():
    atributos_entrada = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    atributos_saida = np.array([0])
    num_de_camadas = 4
    num_de_neuronios_por_camada_oculta = 12
    rede = Rede_Neural(atributos_entrada, atributos_saida, num_de_camadas, num_de_neuronios_por_camada_oculta,
                       bd_vinho)
    return rede
