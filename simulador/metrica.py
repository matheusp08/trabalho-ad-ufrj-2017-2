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

        self.media_esp = [0] * 6                           # lista com a media de cada esperanca

        self.var_nq1 = [-1] * (n_rodadas +1)
        self.var_nq2 = [-1] * (n_rodadas +1)
        self.var_ns1 = [-1] * (n_rodadas +1)
        self.var_ns2 = [-1] * (n_rodadas +1)
        self.var_w1 = [-1] * (n_rodadas + 1)
        self.var_w2 = [-1] * (n_rodadas + 1)

        self.media_var = [0] * 6                           # lista com a media de cada variancia

        self.dp_ns1 = [-1] * (n_rodadas + 1)
        self.dp_ns2 = [-1] * (n_rodadas + 1)
        self.dp_nq1 = [-1] * (n_rodadas + 1)
        self.dp_nq2 = [-1] * (n_rodadas + 1)
        self.dp_w1 = [-1] * (n_rodadas + 1)
        self.dp_w2 = [-1] * (n_rodadas + 1)

        self.fregueses_por_rodada = fregueses_por_rodada
        self.n_rodadas = n_rodadas

    def acumula_generico(self, valor, rodada, tipo):
        '''Adicionando um valor especifico no seu acumulador (Formula generica para w1, w2, nq1, nq2, etc)
        '''

    def acumula_x1(self, x1, rodada):
        '''
        '''
        self.x1[rodada].append(x1)
    
    def acumula_x2(self, x2, rodada):
        '''
        '''
        self.x2[rodada].append(x2)
    
    def acumula_nq1(self, nq1, rodada):
        '''
        '''
        self.nq1[rodada].append(nq1)

    def acumula_nq2(self, nq2, rodada):
        '''
        '''
        self.nq2[rodada].append(nq2)

    def acumula_ns1(self, ns1, rodada):
        '''
        '''
        self.ns1[rodada].append(ns1)

    def acumula_ns2(self, ns2, rodada):
        '''
        '''
        self.ns2[rodada].append(ns2)

    def acumula_w1(self, w1, rodada):
        '''Adicionando o tempo de espera na fila 1 de um fregues na lista. (Nao e feito o somatorio)
        '''
        self.w1[rodada].append(w1)

    def acumula_w2(self, w2, rodada):
        '''Adicionando o tempo de espera na fila 2 de um fregues na lista. (Nao e feito o somatorio)
        '''
        self.w2[rodada].append(w2)

    def calcula_esp(self):
        """ Calcula os valores das esperancas
        """
        tabela_esperancas = PrettyTable()
        tabela_esperancas.add_column("", ["E[W1]", "E[W2]", "E[Nq1]", "E[Nq2]", "E[Ns1]", "E[Ns2]"])

        w1_med_acumulada = 0
        w2_med_acumulada = 0
        nq1_med_acumulada = 0
        nq2_med_acumulada = 0
        ns1_med_acumulada = 0
        ns2_med_acumulada = 0

        for rodada in range(1, self.n_rodadas+1):
            w1_med = round(sum(self.w1[rodada])/self.fregueses_por_rodada, 4)
            w2_med = round(sum(self.w2[rodada])/self.fregueses_por_rodada, 4)
            nq1_med = round(sum(self.nq1[rodada])/self.fregueses_por_rodada, 4)
            nq2_med = round(sum(self.nq2[rodada])/self.fregueses_por_rodada, 4)
            ns1_med = round(sum(self.ns1[rodada])/self.fregueses_por_rodada, 4)
            ns2_med = round(sum(self.ns2[rodada])/self.fregueses_por_rodada, 4)

            tabela_esperancas.add_column("rodada_"+str(rodada), [w1_med, w2_med, nq1_med, nq2_med, ns1_med, ns2_med])

            w1_med_acumulada += w1_med
            w2_med_acumulada += w2_med
            nq1_med_acumulada += nq1_med
            nq2_med_acumulada += nq2_med
            ns1_med_acumulada += ns1_med
            ns2_med_acumulada += ns2_med

        self.media_esp = [w1_med_acumulada, w2_med_acumulada, nq1_med_acumulada, nq2_med_acumulada, ns1_med_acumulada, ns2_med_acumulada]
        self.media_esp = [round(e/self.n_rodadas, 5) for e in self.media_esp]
        tabela_esperancas.add_column("Media", self.media_esp)
        print(tabela_esperancas)

    def calcula_var(self):
        ''' Calcula os valores das variancias e desvios padroes de w1 e w2
        '''
        tabela_variancias = PrettyTable()
        tabela_variancias.add_column("", ["Var[W1]", "Var[W2]", "Var[Nq1]", "Var[Nq2]", "Var[Ns1]", "Var[Ns2]"])

        w1_var_total = 0
        w2_var_total = 0
        nq1_var_total = 0
        nq2_var_total = 0
        ns1_var_total = 0
        ns2_var_total = 0


        for rodada in range(1,self.n_rodadas+1):
            # Essas variaveis acumulado_XX vao representar o (Dado Amostral - Media Amostral)**2
            acumulado_w1 = 0
            acumulado_w2 = 0
            acumulado_nq1 = 0
            acumulado_nq2 = 0
            acumulado_ns1 = 0
            acumulado_ns2 = 0

            w1_med = sum(self.w1[rodada])/self.fregueses_por_rodada
            w2_med = sum(self.w2[rodada])/self.fregueses_por_rodada
            ns1_med = sum(self.ns1[rodada])/self.fregueses_por_rodada
            ns2_med = sum(self.ns2[rodada])/self.fregueses_por_rodada
            nq1_med = sum(self.nq1[rodada])/self.fregueses_por_rodada
            nq2_med = sum(self.nq2[rodada])/self.fregueses_por_rodada

            # Fazendo o somatorio do quadrado da diferenca entre cada dado amostral e metrica_med (Lembrando que cada metrica_med eh acumulado e nao medio real ainda)
            for i in range(len(self.w1[rodada])):
                acumulado_w1 += (self.w1[rodada][i] - w1_med) ** 2

            for j in range(len(self.w2[rodada])):
                acumulado_w2 += (self.w2[rodada][j] - w2_med) ** 2

            for k in range(len(self.nq1[rodada])):
                acumulado_nq1 += (self.nq1[rodada][k] - nq1_med) ** 2

            for z in range(len(self.nq2[rodada])):
                acumulado_nq2 += (self.nq2[rodada][z] - nq2_med) ** 2

            for l in range(len(self.ns1[rodada])):
                acumulado_ns1 += (self.ns1[rodada][l] - ns1_med) ** 2

            for m in range(len(self.ns2[rodada])):
                acumulado_ns2 += (self.ns2[rodada][m] - ns2_med) ** 2

            # Realizando ultimo passo da formula da VAR: dividir o somatorio por n-1
            self.var_w1[rodada] = acumulado_w1 / (self.fregueses_por_rodada - 1)
            self.var_w2[rodada] = acumulado_w2 / (self.fregueses_por_rodada - 1)
            self.var_nq2[rodada] = acumulado_nq2 / (self.fregueses_por_rodada - 1)
            self.var_nq1[rodada] = acumulado_nq1 / (self.fregueses_por_rodada - 1)
            self.var_ns2[rodada] = acumulado_ns2 / (self.fregueses_por_rodada - 1)
            self.var_ns1[rodada] = acumulado_ns1 / (self.fregueses_por_rodada - 1)
            self.dp_w1[rodada] = np.sqrt(self.var_w1[rodada])
            self.dp_w2[rodada] = np.sqrt(self.var_w2[rodada])
            self.dp_nq1[rodada] = np.sqrt(self.var_nq1[rodada])
            self.dp_nq2[rodada] = np.sqrt(self.var_nq2[rodada])
            self.dp_ns1[rodada] = np.sqrt(self.var_ns1[rodada])
            self.dp_ns2[rodada] = np.sqrt(self.var_ns2[rodada])

            tabela_variancias.add_column("rodada_"+str(rodada), [round(self.var_w1[rodada], 5),
                                                                 round(self.var_w2[rodada], 5),
                                                                 round(self.var_nq1[rodada], 5),
                                                                 round(self.var_nq2[rodada], 5),
                                                                 round(self.var_ns1[rodada], 5),
                                                                 round(self.var_ns2[rodada], 5)])
            w1_var_total += self.var_w1[rodada]
            w2_var_total += self.var_w2[rodada]
            nq1_var_total += self.var_nq1[rodada]
            nq2_var_total += self.var_nq2[rodada]
            ns1_var_total += self.var_ns1[rodada]
            ns2_var_total += self.var_ns2[rodada]

        self.media_var = [w1_var_total, w2_var_total, nq1_var_total, nq2_var_total, ns1_var_total, ns2_var_total]
        self.media_var = [round(v/self.n_rodadas, 5) for v in self.media_var]

        tabela_variancias.add_column("Media", self.media_var)
        print(tabela_variancias)

    def calcula_ic(self):
        """ Para o trabalho, calculamos o intervalo de confiança de 95% usando a t-Student
            Para um grau de liberdade muito grande, a t-Student se aproxima da normal unitária (Z é N(0,1))
            P(Z <= 1.96) = 0.975 (1 - 0.05/2)
        """

        raiz_n_rodadas = math.sqrt(self.n_rodadas)
        z = 1.96

        w1_dp_med = sum(self.dp_w1) / self.n_rodadas
        w2_dp_med = sum(self.dp_w2) / self.n_rodadas
        nq1_dp_med = sum(self.dp_nq1) / self.n_rodadas
        nq2_dp_med = sum(self.dp_nq2) / self.n_rodadas
        ns1_dp_med = sum(self.dp_ns1) / self.n_rodadas
        ns2_dp_med = sum(self.dp_ns2) / self.n_rodadas

        w1_ic = z * w1_dp_med / raiz_n_rodadas
        w2_ic = z * w2_dp_med / raiz_n_rodadas
        nq1_ic = z * nq1_dp_med / raiz_n_rodadas
        nq2_ic = z * nq2_dp_med / raiz_n_rodadas
        ns1_ic = z * ns1_dp_med / raiz_n_rodadas
        ns2_ic = z * ns2_dp_med / raiz_n_rodadas

        w1_med = self.media_esp[0]
        w2_med = self.media_esp[1]
        nq1_med = self.media_esp[2]
        nq2_med = self.media_esp[3]
        ns1_med = self.media_esp[4]
        ns2_med = self.media_esp[5]

        print(" W1 - IC entre", (w1_med - w1_ic), "e", (w1_med + w1_ic))
        print(" W2 - IC entre", (w2_med - w2_ic), "e", (w2_med + w2_ic))
        print("Nq1 - IC entre", (nq1_med - nq1_ic), "e", (nq1_med + nq1_ic))
        print("Nq2 - IC entre", (nq2_med - nq2_ic), "e", (nq2_med + nq2_ic))
        print("Ns1 - IC entre", (ns1_med - ns1_ic), "e", (ns1_med + ns1_ic))
        print("Ns2 - IC entre", (ns2_med - ns2_ic), "e", (ns2_med + ns2_ic))
