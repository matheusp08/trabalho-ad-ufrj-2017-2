""" Modulo Plot
"""
import matplotlib.pyplot as plt
import numpy as np

class Plot:
    """ Classe Plot
    """
    def __init__(self):
        pass

    def desenha_grafico(self, dados, xLabel, yLabel):
        """ Funcao para desenhar os graficos
            Args:
                dados: vetor com os valores a serem plotados
                xLabel: texto do eixo x
                yLabel: texto do eixo y
        """
        tamanho = len(dados)
        fator = 100
        plt.plot(dados)
        plt.xticks(np.arange(0, tamanho + 1, fator))
        plt.ylabel(yLabel)
        plt.xlabel(xLabel)
        plt.show()