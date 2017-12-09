""" Modulo Metricas
"""
import numpy as np
import math
from prettytable import PrettyTable

class Metrica:
    """ Classe que calcula as metricas da simulacao
    """
    def __init__(self, n_rodadas, fregueses_por_rodada):
        # Criando matrizes para guardar cada valor de w1 (multiplos valores) por rodada. 
        self.x1 = [[] for _ in range(n_rodadas+1)]
        self.x2 = [[] for _ in range(n_rodadas+1)]
        self.w1 = [[] for _ in range(n_rodadas+1)]
        self.w2 = [[] for _ in range(n_rodadas+1)]
        self.nq1 = [[] for _ in range(n_rodadas+1)]
        self.nq2 = [[] for _ in range(n_rodadas+1)]
        self.ns1 = [[] for _ in range(n_rodadas+1)]
        self.ns2 = [[] for _ in range(n_rodadas+1)]

        self.media_esp = [0] * 8                           # lista com a media de cada esperanca

        self.var_nq1 = [-1] * (n_rodadas +1)
        self.var_nq2 = [-1] * (n_rodadas +1)
        self.var_ns1 = [-1] * (n_rodadas +1)
        self.var_ns2 = [-1] * (n_rodadas +1)
        self.var_w1 = [-1] * (n_rodadas + 1)
        self.var_w2 = [-1] * (n_rodadas + 1)
        self.var_x1 = [-1] * (n_rodadas + 1)
        self.var_x2 = [-1] * (n_rodadas + 1)

        self.media_var = [0] * 8                           # lista com a media de cada variancia

        self.dp_ns1 = [-1] * (n_rodadas + 1)
        self.dp_ns2 = [-1] * (n_rodadas + 1)
        self.dp_nq1 = [-1] * (n_rodadas + 1)
        self.dp_nq2 = [-1] * (n_rodadas + 1)
        self.dp_w1 = [-1] * (n_rodadas + 1)
        self.dp_w2 = [-1] * (n_rodadas + 1)
        self.dp_x1 = [-1] * (n_rodadas + 1)
        self.dp_x2 = [-1] * (n_rodadas + 1)

        self.fregueses_por_rodada = fregueses_por_rodada
        self.n_rodadas = n_rodadas

    def acumula_x1(self, x1, rodada):
        """ Funcao para acumular tempo de servico 1
        """
        self.x1[rodada].append(x1)

    def acumula_x2(self, x2, rodada):
        """ Funcao para acumular o tempo de servico 2
        """
        self.x2[rodada].append(x2)

    def acumula_nq1(self, nq1, rodada):
        """ Funcao para acumular nq1
        """
        self.nq1[rodada].append(nq1)

    def acumula_nq2(self, nq2, rodada):
        """ Funcao para acumular nq2
        """
        self.nq2[rodada].append(nq2)

    def acumula_ns1(self, ns1, rodada):
        """ Funcao para acumular ns1
        """
        self.ns1[rodada].append(ns1)

    def acumula_ns2(self, ns2, rodada):
        """ Funcao para acumular ns2
        """
        self.ns2[rodada].append(ns2)

    def acumula_w1(self, w1, rodada):
        """ Funcao para acumular w1
        """
        self.w1[rodada].append(w1)

    def acumula_w2(self, w2, rodada):
        """ Funcao para acumular w2
        """
        self.w2[rodada].append(w2)

    def calcula_esp(self):
        """ Calcula os valores das esperancas
        """
        tabela_esperancas = PrettyTable()
        tabela_esperancas.add_column("", ["E[W1]", "E[W2]", "E[X1]", "E[X2]", "E[Nq1]", "E[Nq2]", "E[Ns1]", "E[Ns2]"])

        x1_med_acumulada = 0
        x2_med_acumulada = 0
        w1_med_acumulada = 0
        w2_med_acumulada = 0
        nq1_med_acumulada = 0
        nq2_med_acumulada = 0
        ns1_med_acumulada = 0
        ns2_med_acumulada = 0

        for rodada in range(1, self.n_rodadas+1):
            x1_med = sum(self.x1[rodada])/self.fregueses_por_rodada
            x2_med = sum(self.x2[rodada])/self.fregueses_por_rodada
            w1_med = sum(self.w1[rodada])/self.fregueses_por_rodada
            w2_med = sum(self.w2[rodada])/self.fregueses_por_rodada
            nq1_med = sum(self.nq1[rodada])/self.fregueses_por_rodada
            nq2_med = sum(self.nq2[rodada])/self.fregueses_por_rodada
            ns1_med = sum(self.ns1[rodada])/self.fregueses_por_rodada
            ns2_med = sum(self.ns2[rodada])/self.fregueses_por_rodada

            tabela_esperancas.add_column("rodada_"+str(rodada), [w1_med, w2_med, x1_med, x2_med, nq1_med, nq2_med, ns1_med, ns2_med])

            x1_med_acumulada += x1_med
            x2_med_acumulada += x2_med
            w1_med_acumulada += w1_med
            w2_med_acumulada += w2_med
            nq1_med_acumulada += nq1_med
            nq2_med_acumulada += nq2_med
            ns1_med_acumulada += ns1_med
            ns2_med_acumulada += ns2_med

        self.media_esp = [w1_med_acumulada, w2_med_acumulada, x1_med_acumulada, x2_med_acumulada, nq1_med_acumulada, nq2_med_acumulada, ns1_med_acumulada, ns2_med_acumulada]
        self.media_esp = [e/self.n_rodadas for e in self.media_esp]
        tabela_esperancas.add_column("Media", self.media_esp)
        print(tabela_esperancas)

    def calcula_var(self):
        ''' Calcula os valores das variancias e desvios padroes de w1 e w2
        '''
        tabela_variancias = PrettyTable()
        tabela_variancias.add_column("", ["Var[W1]", "Var[W2]", "Var[X1]", "Var[X2]", "Var[Nq1]", "Var[Nq2]", "Var[Ns1]", "Var[Ns2]"])

        w1_var_total = 0
        w2_var_total = 0
        x1_var_total = 0
        x2_var_total = 0
        nq1_var_total = 0
        nq2_var_total = 0
        ns1_var_total = 0
        ns2_var_total = 0

        for rodada in range(1, self.n_rodadas+1):
            w1_med = sum(self.w1[rodada])/self.fregueses_por_rodada
            w2_med = sum(self.w2[rodada])/self.fregueses_por_rodada
            x1_med = sum(self.x1[rodada])/self.fregueses_por_rodada
            x2_med = sum(self.x2[rodada])/self.fregueses_por_rodada
            ns1_med = sum(self.ns1[rodada])/self.fregueses_por_rodada
            ns2_med = sum(self.ns2[rodada])/self.fregueses_por_rodada
            nq1_med = sum(self.nq1[rodada])/self.fregueses_por_rodada
            nq2_med = sum(self.nq2[rodada])/self.fregueses_por_rodada

            self.var_w1[rodada] = (w1_med - self.media_esp[0]) ** 2 / (self.fregueses_por_rodada - 1)
            self.var_w2[rodada] = (w2_med - self.media_esp[1]) ** 2 / (self.fregueses_por_rodada - 1)
            self.var_x1[rodada] = (x1_med - self.media_esp[2]) ** 2 / (self.fregueses_por_rodada - 1)
            self.var_x2[rodada] = (x2_med - self.media_esp[3]) ** 2 / (self.fregueses_por_rodada - 1)
            self.var_nq1[rodada] = (nq1_med - self.media_esp[4]) ** 2 / (self.fregueses_por_rodada - 1)
            self.var_nq2[rodada] = (nq2_med - self.media_esp[5]) ** 2 / (self.fregueses_por_rodada - 1)
            self.var_ns1[rodada] = (ns1_med - self.media_esp[6]) ** 2 / (self.fregueses_por_rodada - 1)
            self.var_ns2[rodada] = (ns2_med - self.media_esp[7]) ** 2 / (self.fregueses_por_rodada - 1)

            self.dp_w1[rodada] = np.sqrt(self.var_w1[rodada])
            self.dp_w2[rodada] = np.sqrt(self.var_w2[rodada])
            self.dp_x1[rodada] = np.sqrt(self.var_x1[rodada])
            self.dp_x2[rodada] = np.sqrt(self.var_x2[rodada])
            self.dp_nq1[rodada] = np.sqrt(self.var_nq1[rodada])
            self.dp_nq2[rodada] = np.sqrt(self.var_nq2[rodada])
            self.dp_ns1[rodada] = np.sqrt(self.var_ns1[rodada])
            self.dp_ns2[rodada] = np.sqrt(self.var_ns2[rodada])

            tabela_variancias.add_column("rodada_"+str(rodada), [self.var_w1[rodada],
                                                                 self.var_w2[rodada],
                                                                 self.var_x1[rodada],
                                                                 self.var_x2[rodada],
                                                                 self.var_nq1[rodada],
                                                                 self.var_nq2[rodada],
                                                                 self.var_ns1[rodada],
                                                                 self.var_ns2[rodada]])
            w1_var_total += self.var_w1[rodada]
            w2_var_total += self.var_w2[rodada]
            x1_var_total += self.var_x1[rodada]
            x2_var_total += self.var_x2[rodada]
            nq1_var_total += self.var_nq1[rodada]
            nq2_var_total += self.var_nq2[rodada]
            ns1_var_total += self.var_ns1[rodada]
            ns2_var_total += self.var_ns2[rodada]

        self.media_var = [w1_var_total, w2_var_total, x1_var_total, x2_var_total, nq1_var_total, nq2_var_total, ns1_var_total, ns2_var_total]
        self.media_var = [v/self.n_rodadas for v in self.media_var]

        tabela_variancias.add_column("Media", self.media_var)
        print(tabela_variancias)
        print('\n')

    def calcula_ic(self):
        """ Para o trabalho, calculamos o intervalo de confiança de 95% usando a t-Student
        """

        raiz_n_rodadas = math.sqrt(self.n_rodadas)
        z = 1.96

        # compensando primeira posicao do vetor com valor -1 somando 1
        w1_dp_med = (sum(self.dp_w1)+1) / self.n_rodadas
        w2_dp_med = (sum(self.dp_w2)+1) / self.n_rodadas
        # x1_dp_med = (sum(self.dp_x1)+1) / self.n_rodadas
        # x2_dp_med = (sum(self.dp_x2)+1) / self.n_rodadas
        # nq1_dp_med = sum(self.dp_nq1+1) / self.n_rodadas
        # nq2_dp_med = sum(self.dp_nq2+1) / self.n_rodadas
        # ns1_dp_med = sum(self.dp_ns1+1) / self.n_rodadas
        # ns2_dp_med = sum(self.dp_ns2+1) / self.n_rodadas

        w1_ic = z * w1_dp_med / raiz_n_rodadas
        w2_ic = z * w2_dp_med / raiz_n_rodadas
        # x1_ic = z * x1_dp_med / raiz_n_rodadas
        # x2_ic = z * x2_dp_med / raiz_n_rodadas
        # nq1_ic = z * nq1_dp_med / raiz_n_rodadas
        # nq2_ic = z * nq2_dp_med / raiz_n_rodadas
        # ns1_ic = z * ns1_dp_med / raiz_n_rodadas
        # ns2_ic = z * ns2_dp_med / raiz_n_rodadas

        w1_med = self.media_esp[0]
        w2_med = self.media_esp[1]
        # x1_med = self.media_esp[2]
        # x2_med = self.media_esp[3]
        # nq1_med = self.media_esp[4]
        # nq2_med = self.media_esp[5]
        # ns1_med = self.media_esp[6]
        # ns2_med = self.media_esp[7]

        print(" W1 - IC entre", (w1_med - w1_ic), "e", (w1_med + w1_ic), "- w1_ic", w1_ic)
        print(" W2 - IC entre", (w2_med - w2_ic), "e", (w2_med + w2_ic), "- w2_ic", w2_ic)
        # print(" X1 - IC entre", (x1_med - x1_ic), "e", (x1_med + x1_ic), "- x1_ic", x1_ic)
        # print(" X2 - IC entre", (x2_med - x2_ic), "e", (x2_med + x2_ic), "- x2_ic", x2_ic)
        # print("Nq1 - IC entre", (nq1_med - nq1_ic), "e", (nq1_med + nq1_ic), "- nq1_ic", nq1_ic)
        # print("Nq2 - IC entre", (nq2_med - nq2_ic), "e", (nq2_med + nq2_ic), "- nq2_ic", nq2_ic)
        # print("Ns1 - IC entre", (ns1_med - ns1_ic), "e", (ns1_med + ns1_ic), "- ns1_ic", ns1_ic)
        # print("Ns2 - IC entre", (ns2_med - ns2_ic), "e", (ns2_med + ns2_ic), "- ns2_ic", ns2_ic)
        print("\n")
