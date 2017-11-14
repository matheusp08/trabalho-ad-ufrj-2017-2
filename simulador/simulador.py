"""Modulo Simulador
"""

from fila import Fila
from fregues import Fregues
from utils import Utils

class Simulador:
    """Classe do simulador
    Attributes:
        taxa: taxa de entrada das filas
        t_student: distribuicao para intervalo de confianca de 95%
    """
    def __init__(self):
        self.taxa = Utils.gera_taxa_exp(0.2)
        self.t_student = Utils.get_distribuicao_t_student()

    def executar(self, n_rodadas):
        """Funcao de execucao do simulador
        Args:
            n_rodadas: numero de rodadas da simulacao.
        """
        print("Numero de rodadas: %d" % n_rodadas)
        print("T-student 95 por cento intervalo de confianca: %f" % self.t_student)
        Fila("FCFS", 1, self.taxa).imprime_parametros()
        Fila("FCFS", 2, self.taxa).imprime_parametros()
        Fregues().imprime_parametros()

Simulador().executar(100)
