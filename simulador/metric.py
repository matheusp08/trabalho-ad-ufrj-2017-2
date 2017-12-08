""" Modulo Metricas
"""
import numpy as np
import math

class Metric:
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
        self.var_nq1 = [-1] * (n_rodadas +1)
        self.var_nq2 = [-1] * (n_rodadas +1)
        self.var_ns1 = [-1] * (n_rodadas +1)
        self.var_ns2 = [-1] * (n_rodadas +1)
        self.var_w1 = [-1] * (n_rodadas + 1)
        self.var_w2 = [-1] * (n_rodadas + 1)
        self.dp_ns1 = [-1] * (n_rodadas + 1)
        self.dp_ns2 = [-1] * (n_rodadas + 1)
        self.dp_nq1 = [-1] * (n_rodadas + 1)
        self.dp_nq2 = [-1] * (n_rodadas + 1)
        self.dp_w1 = [-1] * (n_rodadas + 1)
        self.dp_w2 = [-1] * (n_rodadas + 1)
        self.fregueses_por_rodada = fregueses_por_rodada
        self.n_rodadas = n_rodadas
        self.contador = 1

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
        for rodada in range(1,self.n_rodadas+1):
            w1_med = sum(self.w1[rodada])/self.fregueses_por_rodada
            w2_med = sum(self.w2[rodada])/self.fregueses_por_rodada
            ns1_med = sum(self.ns1[rodada])/self.fregueses_por_rodada
            ns2_med = sum(self.ns2[rodada])/self.fregueses_por_rodada
            nq1_med = sum(self.nq1[rodada])/self.fregueses_por_rodada
            nq2_med = sum(self.nq2[rodada])/self.fregueses_por_rodada

            # Prints para Debug
            print("[Rodada %d]" % rodada)
            print("- E[W1]: %.4f" % w1_med)
            print("- E[W2]: %.4f" % w2_med)
            print("- E[Nq1]: %.4f" % nq1_med)
            print("- E[Nq2]: %.4f" % nq2_med)
            print("- E[Ns1]: %.4f" % ns1_med)
            print("- E[Ns2]: %.4f" % ns2_med)

    def calcula_var(self, rodada):
        ''' Calcula os valores das variancias e desvios padroes de w1 e w2
        '''
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

        # Prints para Debug
        print('[Rodada ', rodada , ']\n- Var(w1): ', self.var_w1[rodada], '.\n- Var(w2): ', self.var_w2[rodada] , '.', sep='')
        print('- Var(Nq1): ', self.var_nq1[rodada], '.\n- Var(Nq2): ', self.var_nq2[rodada] , '.', sep='')
        print('- Var(Ns1): ', self.var_ns1[rodada], '.\n- Var(Ns2): ', self.var_ns2[rodada] , '.\n', sep='')