""" Modulo Metricas
"""
import numpy as np
import math

class Metric:
    def __init__(self, n_rodadas, fregueses_por_rodada):
        # Criando matrizes para guardar cada valor de w1 (multiplos valores) por rodada.
        self.w1 = [[]] * (n_rodadas + 1) 
        self.w2 = [[]] * (n_rodadas + 1)
        self.var_w1 = [-1] * (n_rodadas + 1)
        self.var_w2 = [-1] * (n_rodadas + 1)
        self.dp_w1 = [-1] * (n_rodadas + 1)
        self.dp_w2 = [-1] * (n_rodadas + 1)
        self.fregueses_por_rodada = fregueses_por_rodada
    
    def acumula_w1(self, w1, rodada):
        '''Adicionando o tempo de espera na fila 1 de um fregues na lista. (Nao e feito o somatorio)
        '''
        np.append(self.w1[rodada], w1)

    def acumula_w2(self, w2, rodada):
        '''Adicionando o tempo de espera na fila 2 de um fregues na lista. (Nao e feito o somatorio)
        '''
        np.append(self.w2[rodada], w2)

    def calcula_var(self, rodada, w1_med, w2_med):
        '''Calcula os valores das variancias e desvios padroes de w1 e w2
        '''
        acumulado_w1 = 0
        acumulado_w2 = 0
        var_w1 = 0
        var_w2 = 0

        # Fazendo o somatorio do quadrado da diferenca entre cada w1 e w1_med
        for i in range(len(self.w1[rodada])):
            acumulado_w1 += (self.w1[rodada][i] - w1_med) ** 2

        # Fazendo o somatorio do quadrado da diferenca entre cada w1 e w1_med
        for j in range(len(self.w2[rodada])):
            acumulado_w2 += (self.w2[rodada][j] - w2_med) ** 2
        
        # Realizando ultimo passo da formula da VAR: dividir o somatorio por n-1
        self.var_w1[rodada] = acumulado_w1 / (self.fregueses_por_rodada - 1)
        self.var_w2[rodada] = acumulado_w2 / (self.fregueses_por_rodada - 1)
        self.dp_w1[rodada] = np.sqrt(var_w1)
        self.dp_w2[rodada] = np.sqrt(var_w2)

        print('[Rodada ', rodada , ']\n- Variancia w1: ', var_w1, '.\n- Variancia w2: ', var_w2 , '.', sep='')