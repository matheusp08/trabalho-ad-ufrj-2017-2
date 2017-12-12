""" Modulo Plot
"""
import matplotlib.pyplot as plt
import numpy as np
from fila import Fila

class Plot:
    """ Classe Plot
    """
    def __init__(self):
        self.w1_acumulado = 0
        self.nq1_acumulado = 0
        self.ns1_acumulado = 0
        self.w2_acumulado = 0
        self.nq2_acumulado = 0
        self.ns2_acumulado = 0

        self.w1 = []
        self.nq1 = []
        self.ns1 = []
        self.w2 = []
        self.nq2 = []
        self.ns2 = []

    def desenha(self, intervalo, n_rodadas, n_fregueses, n_transiente, rho):
        """ Funcao para desenhar as metricas
        """

        labelx = "Numero de fregueses"
        params = str(n_rodadas) +"_"+ str(n_fregueses) +"_"+ str(n_transiente) +"_"+ str(rho)
        
        plt.figure(params)
        
        titulo = str(n_rodadas) + " rodadas; " + str(n_fregueses) +" fregueses; Fase transiente: "+ str(n_transiente) +"; rho = " + str(rho)
        plt.suptitle(titulo, fontsize=18)
        
        # plt.figure("E[W1] x " + labelx + params)
        plt.subplot(321)
        plt.plot(self.w1)
        plt.xticks(np.arange(0, len(self.w1) + 1, intervalo))
        plt.ylabel("Tempo medio de espera da fila 1")
        plt.xlabel(labelx)

        # plt.figure("E[W2] x " + labelx + params)
        plt.subplot(322)        
        plt.plot(self.w2)
        plt.xticks((np.arange(0, len(self.w2) + 1, intervalo)))
        plt.ylabel("Tempo medio de espera da fila 2")
        plt.xlabel(labelx)

        # plt.figure("E[Nq1] x " + labelx + params)
        plt.subplot(323)
        plt.plot(self.nq1)
        plt.xticks(np.arange(0, len(self.nq1) + 1, intervalo))
        plt.ylabel("Media do tamanho da fila 1")
        plt.xlabel(labelx)

        # plt.figure("E[Nq2] x " + labelx + params)
        plt.subplot(324)
        plt.plot(self.nq2)
        plt.xticks((np.arange(0, len(self.nq2) + 1, intervalo)))
        plt.ylabel("Media do tamanho da fila 2")
        plt.xlabel(labelx)

        # plt.figure("E[Ns1] x " + labelx + params)
        plt.subplot(325)
        plt.plot(self.ns1)
        plt.xticks((np.arange(0, len(self.ns1) + 1, intervalo)))
        plt.ylabel("Utilizacao da fila 1")
        plt.xlabel(labelx)

        # plt.figure("E[Ns2] x " + labelx + params)
        plt.subplot(326)
        plt.plot(self.ns2)
        plt.xticks((np.arange(0, len(self.ns2) + 1, intervalo)))
        plt.ylabel("Utilizacao da fila 2")
        plt.xlabel(labelx)

        figure = plt.gcf()
        figure.set_size_inches(26, 18)
        plt.savefig("graficos/" + params + ".png", dpi=500)
        plt.show()
