""" Modulo Plot
"""
import matplotlib.pyplot as plt
import numpy as np
from fila import Fila

class Plot:
    """ Classe Plot
    """
    figuras = 6

    def __init__(self, n_rodadas, fregueses_por_rodada, n_transiente, pontos):
        self.ns1 = []
        self.nq1 = []
        self.w1 = []
        self.ns2 = []
        self.nq2 = []
        self.w2 = []
        self.fregueses_por_rodada = fregueses_por_rodada
        self.n_rodadas = n_rodadas
        self.n_transiente = n_transiente
        self.intervalo = (fregueses_por_rodada + n_transiente) / pontos

    def desenha(self, tamanho):
        """ Funcao para desenhar as metricas
        """
        plt.figure(1)
        plt.plot(self.ns1)
        plt.figure(2)
        plt.plot(self.ns2)
        plt.show()

    def desenha_grafico(self, dados, x_label, y_label):
        """ Funcao para desenhar os graficos
            Args:
                dados: vetor com os valores a serem plotados
                xLabel: texto do eixo x
                yLabel: texto do eixo y
        """
        tamanho = len(dados)
        fator = self.fregueses_por_rodada * self.n_rodadas * 0.01
        plt.plot(dados)
        plt.xticks(np.arange(0, tamanho + 1, fator))
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.show()
