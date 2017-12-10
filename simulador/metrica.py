""" Modulo Metricas
"""
import math
import numpy as np
from scipy.stats import chi2
from prettytable import PrettyTable

class Metrica:
    """ Classe que calcula as metricas da simulacao
    """
    def __init__(self, n_rodadas, fregueses_por_rodada):
        # FILA 1
        # Matriz com a amostra de cada metrica por rodada
        self.x1 = [[] for _ in range(n_rodadas+1)]
        self.w1 = [[] for _ in range(n_rodadas+1)]
        self.nq1 = [[] for _ in range(n_rodadas+1)]
        self.ns1 = [[] for _ in range(n_rodadas+1)]
        self.n1 = [[] for _ in range(n_rodadas+1)]
        self.t1 = [[] for _ in range(n_rodadas+1)]

        # lista com a esperanca de cada metrica por rodada
        self.x1_med_rodada = [0] * (n_rodadas + 1)
        self.w1_med_rodada = [0] * (n_rodadas + 1)
        self.nq1_med_rodada = [0] * (n_rodadas + 1)
        self.ns1_med_rodada = [0] * (n_rodadas + 1)
        self.n1_med_rodada = [0] * (n_rodadas + 1)
        self.t1_med_rodada = [0] * (n_rodadas + 1)

        # media total (considerando todas as rodadas) de cada metrica
        self.x1_med_total = 0
        self.w1_med_total = 0
        self.nq1_med_total = 0
        self.ns1_med_total = 0
        self.n1_med_total = 0
        self.t1_med_total = 0

        # variancia das metricas por rodada, considerando (amostra_rodada - media_rodada) / (total amostras - 1)
        self.var_w1_med_rodada = [0] * (n_rodadas + 1)

        # media total das variancias
        self.var_w1_med_total = 0

        # variancia da media das metricas, considerando (media_rodada - media_total) / (total rodadas - 1)
        self.var_x1 = 0
        self.var_w1 = 0
        self.var_nq1 = 0
        self.var_ns1 = 0
        self.var_n1 = 0
        self.var_t1 = 0
        self.var_w1_med = 0

        # desvios padrao
        self.dp_x1 = 0
        self.dp_w1 = 0
        self.dp_nq1 = 0
        self.dp_ns1 = 0
        self.dp_n1 = 0
        self.dp_t1 = 0
        self.dp_w1_med = 0

        # intervalo de confianca
        self.ic_x1 = 0
        self.ic_w1 = 0
        self.ic_nq1 = 0
        self.ic_ns1 = 0
        self.ic_n1 = 0
        self.ic_t1 = 0
        self.ic_w1_med = 0

        # precisao do ic
        self.precisao_x1 = 0
        self.precisao_w1 = 0
        self.precisao_nq1 = 0
        self.precisao_ns1 = 0
        self.precisao_n1 = 0
        self.precisao_t1 = 0
        self.precisao_w1_med = 0

        # FILA 2
        # Matriz com a amostra de cada metrica por rodada
        self.x2 = [[] for _ in range(n_rodadas+1)]
        self.w2 = [[] for _ in range(n_rodadas+1)]
        self.nq2 = [[] for _ in range(n_rodadas+1)]
        self.ns2 = [[] for _ in range(n_rodadas+1)]
        self.n2 = [[] for _ in range(n_rodadas+1)]
        self.t2 = [[] for _ in range(n_rodadas+1)]

        # lista com a esperanca de cada metrica por rodada
        self.x2_med_rodada = [0] * (n_rodadas + 1)
        self.w2_med_rodada = [0] * (n_rodadas + 1)
        self.nq2_med_rodada = [0] * (n_rodadas + 1)
        self.ns2_med_rodada = [0] * (n_rodadas + 1)
        self.n2_med_rodada = [0] * (n_rodadas + 1)
        self.t2_med_rodada = [0] * (n_rodadas + 1)

        # media total (considerando todas as rodadas) de cada metrica
        self.x2_med_total = 0
        self.w2_med_total = 0
        self.nq2_med_total = 0
        self.ns2_med_total = 0
        self.n2_med_total = 0
        self.t2_med_total = 0

        # variancia das metricas por rodada, considerando (amostra_rodada - media_rodada) / (total amostras - 1)
        self.var_w2_med_rodada = [0] * (n_rodadas + 1)

        # media total das variancias
        self.var_w2_med_total = 0

        # variancia da media das metricas, considerando (media_rodada - media_total) / (total rodadas - 1)
        self.var_x2 = 0
        self.var_w2 = 0
        self.var_nq2 = 0
        self.var_ns2 = 0
        self.var_n2 = 0
        self.var_t2 = 0
        self.var_w2_med = 0

        # desvios padrao
        self.dp_x2 = 0
        self.dp_w2 = 0
        self.dp_nq2 = 0
        self.dp_ns2 = 0
        self.dp_n2 = 0
        self.dp_t2 = 0
        self.dp_w2_med = 0

        # intervalo de confianca
        self.ic_x2 = 0
        self.ic_w2 = 0
        self.ic_nq2 = 0
        self.ic_ns2 = 0
        self.ic_n2 = 0
        self.ic_t2 = 0
        self.ic_w2_med = 0

        # precisao do ic
        self.precisao_x2 = 0
        self.precisao_w2 = 0
        self.precisao_nq2 = 0
        self.precisao_ns2 = 0
        self.precisao_n2 = 0
        self.precisao_t2 = 0
        self.precisao_w2_med = 0

        # ic utilizando chi-square
        self.chi2_inferior = 0
        self.chi2_superior = 0
        self.w1_chi2_inferior = 0
        self.w1_chi2_superior = 0
        self.w2_chi2_inferior = 0
        self.w2_chi2_superior = 0
        self.precisao_chi2 = 0

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

    def acumula_n1(self, n1, rodada):
        """ Funcao para acumular n1
        """
        self.n1[rodada].append(n1)

    def acumula_n2(self, n2, rodada):
        """ Funcao para acumular n2
        """
        self.n2[rodada].append(n2)

    def acumula_t1(self, t1, rodada):
        """ Funcao para acumular t1
        """
        self.t1[rodada].append(t1)

    def acumula_t2(self, t2, rodada):
        """ Funcao para acumular t2
        """
        self.t2[rodada].append(t2)

    def calcula(self):
        """ Calcula os valores das esperancas
        """
        # criando header da tabela
        tabela = PrettyTable(["Rodadas",
                              "E[T1]",
                              "E[W1]",
                              "E[X1]",
                              "E[N1]",
                              "E[Nq1]",
                              "E[Ns1]",
                              "E[T2]",
                              "E[W2]",
                              "E[X2]",
                              "E[N2]",
                              "E[Nq2]",
                              "E[Ns2]",
                              "Var[W1]",
                              "Var[W2]"])

        for index in range(1, self.n_rodadas+1):
            # calculando a esperanca das metricas da fila 1
            self.x1_med_rodada[index] = sum(self.x1[index])/self.fregueses_por_rodada
            self.w1_med_rodada[index] = sum(self.w1[index])/self.fregueses_por_rodada
            self.nq1_med_rodada[index] = sum(self.nq1[index])/self.fregueses_por_rodada
            self.ns1_med_rodada[index] = sum(self.ns1[index])/self.fregueses_por_rodada
            self.n1_med_rodada[index] = sum(self.n1[index])/self.fregueses_por_rodada
            self.t1_med_rodada[index] = sum(self.t1[index])/self.fregueses_por_rodada

            # calculando a esperanca das metricas da fila 2
            self.x2_med_rodada[index] = sum(self.x2[index])/self.fregueses_por_rodada
            self.w2_med_rodada[index] = sum(self.w2[index])/self.fregueses_por_rodada
            self.nq2_med_rodada[index] = sum(self.nq2[index])/self.fregueses_por_rodada
            self.ns2_med_rodada[index] = sum(self.ns2[index])/self.fregueses_por_rodada
            self.n2_med_rodada[index] = sum(self.n2[index])/self.fregueses_por_rodada
            self.t2_med_rodada[index] = sum(self.t2[index])/self.fregueses_por_rodada

            # calculo de Var[W1] e Var[W2] para exibir na tabela
            for amostra in range(len(self.w1[index])):
                self.var_w1_med_rodada[index] += (self.w1[index][amostra] - self.w1_med_rodada[index]) ** 2
                self.var_w2_med_rodada[index] += (self.w2[index][amostra] - self.w2_med_rodada[index]) ** 2

            self.var_w1_med_rodada[index] /= (len(self.w1[index]) - 1)
            self.var_w2_med_rodada[index] /= (len(self.w2[index]) - 1)

            tabela.add_row(["rodada_" + str(index),
                            round(self.t1_med_rodada[index], 6),
                            round(self.w1_med_rodada[index], 6),
                            round(self.x1_med_rodada[index], 6),
                            round(self.n1_med_rodada[index], 6),
                            round(self.nq1_med_rodada[index], 6),
                            round(self.ns1_med_rodada[index], 6),
                            round(self.t2_med_rodada[index], 6),
                            round(self.w2_med_rodada[index], 6),
                            round(self.w2_med_rodada[index], 6),
                            round(self.n2_med_rodada[index], 6),
                            round(self.nq2_med_rodada[index], 6),
                            round(self.ns2_med_rodada[index], 6),
                            round(self.var_w1_med_rodada[index], 6),
                            round(self.var_w2_med_rodada[index], 6)])

            # acumulando medias totais
            self.x1_med_total += self.x1_med_rodada[index]
            self.w1_med_total += self.w1_med_rodada[index]
            self.nq1_med_total += self.nq1_med_rodada[index]
            self.ns1_med_total += self.ns1_med_rodada[index]
            self.n1_med_total += self.n1_med_rodada[index]
            self.t1_med_total += self.t1_med_rodada[index]
            self.x2_med_total += self.x2_med_rodada[index]
            self.w2_med_total += self.w2_med_rodada[index]
            self.nq2_med_total += self.nq2_med_rodada[index]
            self.ns2_med_total += self.ns2_med_rodada[index]
            self.n2_med_total += self.n2_med_rodada[index]
            self.t2_med_total += self.t2_med_rodada[index]
            self.var_w1_med_total += self.var_w1_med_rodada[index]
            self.var_w2_med_total += self.var_w2_med_rodada[index]

        # dividindo medias acumuladas pelo total de rodadas e enfim, calculando a media total de cada metrica
        self.x1_med_total /= self.n_rodadas
        self.w1_med_total /= self.n_rodadas
        self.nq1_med_total /= self.n_rodadas
        self.ns1_med_total /= self.n_rodadas
        self.n1_med_total /= self.n_rodadas
        self.t1_med_total /= self.n_rodadas
        self.x2_med_total /= self.n_rodadas
        self.w2_med_total /= self.n_rodadas
        self.nq2_med_total /= self.n_rodadas
        self.ns2_med_total /= self.n_rodadas
        self.n2_med_total /= self.n_rodadas
        self.t2_med_total /= self.n_rodadas
        self.var_w1_med_total /= self.n_rodadas
        self.var_w2_med_total /= self.n_rodadas

        tabela.add_row(["Media",
                        round(self.t1_med_total, 6),
                        round(self.w1_med_total, 6),
                        round(self.x1_med_total, 6),
                        round(self.n1_med_total, 6),
                        round(self.nq1_med_total, 6),
                        round(self.ns1_med_total, 6),
                        round(self.t2_med_total, 6),
                        round(self.w2_med_total, 6),
                        round(self.x2_med_total, 6),
                        round(self.n2_med_total, 6),
                        round(self.nq2_med_total, 6),
                        round(self.ns2_med_total, 6),
                        round(self.var_w1_med_total, 6),
                        round(self.var_w2_med_total, 6)])

        print(tabela, "\n")

        self.calcula_ic()

    def calcula_variancias(self):
        """ Funcao para calcular a variancia das medias das rodadas (amostra = media da rodada)
		    Variancia = somatorio, para todas as amostras, de (amostra - media das amostras) ** 2 dividido por (numero de rodadas - 1)
		"""
        for index in range(1, self.n_rodadas+1):
            self.var_x1 += (self.x1_med_rodada[index] - self.x1_med_total) ** 2
            self.var_w1 += (self.w1_med_rodada[index] - self.w1_med_total) ** 2
            self.var_nq1 += (self.nq1_med_rodada[index] - self.nq1_med_total) ** 2
            self.var_ns1 += (self.ns1_med_rodada[index] - self.ns1_med_total) ** 2
            self.var_n1 += (self.n1_med_rodada[index] - self.n1_med_total) ** 2
            self.var_t1 += (self.t1_med_rodada[index] - self.t1_med_total) ** 2
            self.var_w1_med += (self.var_w1_med_rodada[index] - self.var_w1_med_total) ** 2

            self.var_x2 += (self.x2_med_rodada[index] - self.x2_med_total) ** 2
            self.var_w2 += (self.w2_med_rodada[index] - self.w2_med_total) ** 2
            self.var_nq2 += (self.nq2_med_rodada[index] - self.nq2_med_total) ** 2
            self.var_ns2 += (self.ns2_med_rodada[index] - self.ns2_med_total) ** 2
            self.var_n2 += (self.n2_med_rodada[index] - self.n2_med_total) ** 2
            self.var_t2 += (self.t2_med_rodada[index] - self.t2_med_total) ** 2
            self.var_w2_med += (self.var_w2_med_rodada[index] - self.var_w2_med_total) ** 2

        if self.n_rodadas > 1:
            self.var_x1 /= (self.n_rodadas - 1)
            self.var_w1 /= (self.n_rodadas - 1)
            self.var_nq1 /= (self.n_rodadas - 1)
            self.var_ns1 /= (self.n_rodadas - 1)
            self.var_n1 /= (self.n_rodadas - 1)
            self.var_t1 /= (self.n_rodadas - 1)
            self.var_w1_med /= (self.n_rodadas - 1)

            self.var_x2 /= (self.n_rodadas - 1)
            self.var_w2 /= (self.n_rodadas - 1)
            self.var_nq2 /= (self.n_rodadas - 1)
            self.var_ns2 /= (self.n_rodadas - 1)
            self.var_n2 /= (self.n_rodadas - 1)
            self.var_t2 /= (self.n_rodadas - 1)
            self.var_w2_med /= (self.n_rodadas - 1)

    def calcula_desvios_padrao(self):
        """ Funcao para calcular os desvios padroes das metricas analisadas
        """
        self.dp_x1 = np.sqrt(self.var_x1)
        self.dp_w1 = np.sqrt(self.var_w1)
        self.dp_nq1 = np.sqrt(self.var_nq1)
        self.dp_ns1 = np.sqrt(self.var_ns1)
        self.dp_n1 = np.sqrt(self.var_n1)
        self.dp_t1 = np.sqrt(self.var_t1)
        self.dp_w1_med = np.sqrt(self.var_w1_med)

        self.dp_x2 = np.sqrt(self.var_x2)
        self.dp_w2 = np.sqrt(self.var_w2)
        self.dp_nq2 = np.sqrt(self.var_nq2)
        self.dp_ns2 = np.sqrt(self.var_ns2)
        self.dp_n2 = np.sqrt(self.var_n2)
        self.dp_t2 = np.sqrt(self.var_t2)
        self.dp_w2_med = np.sqrt(self.var_w2_med)

    def calcula_ic(self):
        """ Funcao para calcular os Intervalo de confianca das metricas
            Para o trabalho, calculamos o intervalo de confiança de 95% usando a t-Student
        """
        self.calcula_variancias()
        self.calcula_desvios_padrao()

        raiz_n_rodadas = math.sqrt(self.n_rodadas)
        t_student = 1.96

        # calculando o intervalo de confianca de cada metrica utilizando a t-student
        self.ic_x1 = t_student * self.dp_x1 / raiz_n_rodadas
        self.ic_w1 = t_student * self.dp_w1 / raiz_n_rodadas
        self.ic_nq1 = t_student * self.dp_nq1 / raiz_n_rodadas
        self.ic_ns1 = t_student * self.dp_ns1 / raiz_n_rodadas
        self.ic_n1 = t_student * self.dp_n1 / raiz_n_rodadas
        self.ic_t1 = t_student * self.dp_t1 / raiz_n_rodadas
        self.ic_w1_med = t_student * self.dp_w1_med / raiz_n_rodadas

        self.ic_x2 = t_student * self.dp_x2 / raiz_n_rodadas
        self.ic_w2 = t_student * self.dp_w2 / raiz_n_rodadas
        self.ic_nq2 = t_student * self.dp_nq2 / raiz_n_rodadas
        self.ic_ns2 = t_student * self.dp_ns2 / raiz_n_rodadas
        self.ic_n2 = t_student * self.dp_n2 / raiz_n_rodadas
        self.ic_t2 = t_student * self.dp_t2 / raiz_n_rodadas
        self.ic_w2_med = t_student * self.dp_w2_med / raiz_n_rodadas

        # calculando a precisao de cada metrica
        self.precisao_x1 = round((self.ic_x1 / self.x1_med_total) * 100, 2)
        self.precisao_w1 = round((self.ic_w1 / self.w1_med_total) * 100, 2)
        self.precisao_nq1 = round((self.ic_nq1 / self.nq1_med_total) * 100, 2)
        self.precisao_ns1 = round((self.ic_ns1 / self.ns1_med_total) * 100, 2)
        self.precisao_n1 = round((self.ic_n1 / self.n1_med_total) * 100, 2)
        self.precisao_t1 = round((self.ic_t1 / self.t1_med_total) * 100, 2)
        self.precisao_w1_med = round((self.ic_w1_med / self.var_w1_med_total) * 100, 2)

        self.precisao_x2 = round((self.ic_x2 / self.x2_med_total) * 100, 2)
        self.precisao_w2 = round((self.ic_w2 / self.w2_med_total) * 100, 2)
        self.precisao_nq2 = round((self.ic_nq2 / self.nq2_med_total) * 100, 2)
        self.precisao_ns2 = round((self.ic_ns2 / self.ns2_med_total) * 100, 2)
        self.precisao_n2 = round((self.ic_n2 / self.n2_med_total) * 100, 2)
        self.precisao_t2 = round((self.ic_t2 / self.t2_med_total) * 100, 2)
        self.precisao_w2_med = round((self.ic_w2_med / self.var_w2_med_total) * 100, 2)

		# calculando o intervalo de confianca de V[W1] e V[W2] usando chi-squared
		# eh usada como variancia a media da variancia de todas as rodadas, e n como numero de fregueses por rodada
        alfa = 0.05

        # calculando a inversa da cdf para os limites inferior e superior
        self.chi2_inferior = chi2.ppf(1 - alfa/2, self.fregueses_por_rodada - 1)
        self.chi2_superior  = chi2.ppf(alfa/2, self.fregueses_por_rodada - 1)

        self.w1_chi2_inferior = (self.fregueses_por_rodada - 1) * self.var_w1_med_total / self.chi2_inferior
        self.w1_chi2_superior = (self.fregueses_por_rodada - 1) * self.var_w1_med_total / self.chi2_superior

        self.w2_chi2_inferior = (self.fregueses_por_rodada - 1) * self.var_w2_med_total / self.chi2_inferior
        self.w2_chi2_superior = (self.fregueses_por_rodada - 1) * self.var_w2_med_total / self.chi2_superior

        self.precisao_chi2 = round(((self.chi2_inferior - self.chi2_superior) / (self.chi2_inferior + self.chi2_superior)) * 100, 2)

        tabela = PrettyTable(["Metrica", "Intervalo_inferior", "Intervalo_superior", "precisao"])

        tabela.add_row(["E[T1]", round((self.t1_med_total - self.ic_t1), 6), round((self.t1_med_total + self.ic_t1), 6), str(self.precisao_t1) + "%"])
        tabela.add_row(["E[W1]", round((self.w1_med_total - self.ic_w1), 6), round((self.w1_med_total + self.ic_w1), 6), str(self.precisao_w1) + "%"])
        tabela.add_row(["E[X1]", round((self.x1_med_total - self.ic_x1), 6), round((self.x1_med_total + self.ic_x1), 6), str(self.precisao_x1) + "%"])
        tabela.add_row(["E[N1]", round((self.n1_med_total - self.ic_n1), 6), round((self.n1_med_total + self.ic_n1), 6), str(self.precisao_n1) + "%"])
        tabela.add_row(["E[Nq1]", round((self.nq1_med_total - self.ic_nq1), 6), round((self.nq1_med_total + self.ic_nq1), 6), str(self.precisao_nq1) + "%"])
        tabela.add_row(["E[Ns1]", round((self.ns1_med_total - self.ic_ns1), 6), round((self.ns1_med_total + self.ic_ns1), 6), str(self.precisao_ns1) + "%"])

        tabela.add_row(["E[T2]", round((self.t2_med_total - self.ic_t2), 6), round((self.t2_med_total + self.ic_t2), 6), str(self.precisao_t2) + "%"])
        tabela.add_row(["E[W2]", round((self.w2_med_total - self.ic_w2), 6), round((self.w2_med_total + self.ic_w2), 6), str(self.precisao_w2) + "%"])
        tabela.add_row(["E[X2]", round((self.x2_med_total - self.ic_x2), 6), round((self.x2_med_total + self.ic_x2), 6), str(self.precisao_x2) + "%"])
        tabela.add_row(["E[N2]", round((self.n2_med_total - self.ic_n2), 6), round((self.n2_med_total + self.ic_n2), 6), str(self.precisao_n2) + "%"])
        tabela.add_row(["E[Nq2]", round((self.nq2_med_total - self.ic_nq2), 6), round((self.nq2_med_total + self.ic_nq2), 6), str(self.precisao_nq2) + "%"])
        tabela.add_row(["E[Ns2]", round((self.ns2_med_total - self.ic_ns2), 6), round((self.ns2_med_total + self.ic_ns2), 6), str(self.precisao_ns2) + "%"])

        tabela.add_row(["V[W1] t_student", round((self.var_w1_med_total - self.ic_w1_med), 6), round((self.var_w1_med_total + self.ic_w1_med), 6), str(self.precisao_w1_med) + "%"])
        tabela.add_row(["V[W2] t_student", round((self.var_w2_med_total - self.ic_w2_med), 6), round((self.var_w2_med_total + self.ic_w2_med), 6), str(self.precisao_w2_med) + "%"])
        
        tabela.add_row(["V[W1] chi_square", round(self.w1_chi2_inferior, 6), round(self.w1_chi2_superior, 6), str(self.precisao_chi2) + "%"])
        tabela.add_row(["V[W2] chi_square", round(self.w2_chi2_inferior, 6), round(self.w2_chi2_superior, 6), str(self.precisao_chi2) + "%"])

        print(tabela, "\n")
