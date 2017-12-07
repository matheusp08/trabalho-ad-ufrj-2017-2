""" Modulo Plot
"""
import matplotlib.pyplot as plt
import numpy as np

class Plot:
    """ Classe Plot
    """
    def __init__(self):
        pass

    def desenha_grafico(self, dados, x_label, y_label, n_fregueses):
        """ Funcao para desenhar os graficos
            Args:
                dados: vetor com os valores a serem plotados
                xLabel: texto do eixo x
                yLabel: texto do eixo y
        """
        tamanho = len(dados)
        fator = n_fregueses * 0.01
        plt.plot(dados)
        plt.xticks(np.arange(0, tamanho + 1, fator))
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.show()
