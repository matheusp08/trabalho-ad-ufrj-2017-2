"""Modulo Simulador
"""

from datetime import datetime
from fila import Fila
from fregues import Fregues
from utils import Utils
from evento import Evento, TipoEvento

class Simulador:
    """Classe do simulador
    Attributes:
        taxa: taxa de entrada das filas
        t_student: distribuicao para intervalo de confianca de 95%
    """
    def __init__(self):
        self.taxa = Utils.gera_taxa_exp(0.2)
        self.t_student = Utils.get_distribuicao_t_student()

    def executar(self, n_fregueses, n_rodadas, rho):
        """ Funcao de execucao do simulador
        Args:
            n_fregueses: numero de fregueses
            n_rodadas: numero de rodadas da simulacao.
            rho: taxa
        """
        lambd = rho/2
        taxa_servico = 1
        resultados = []

        inicio = datetime.now()
        for i in range(n_rodadas):
            resultado = self.executar_rodada(n_fregueses, lambd, taxa_servico)
            resultados.append(resultado)
        fim = datetime.now()
        total = fim - inicio

        print("Tempo de execucao: %f" % total)

    def executar_rodada(self, n_fregueses, lambd, taxa_servico):
        """ Metodo responsavel pela execucao de cada rodada
        """
        fila1 = Fila(1)
        fila2 = Fila(2)
        eventos = []
        tempo_atual = 0
        fregueses_servidos = 0
        id_proximo_fregues = 0

        while fregueses_servidos < n_fregueses:
            chegada = Utils.gera_taxa_exp_seed(lambd)
            tempo_atual += chegada

            if id_proximo_fregues < n_fregueses:
                fregues = Fregues(id_proximo_fregues, tempo_atual, lambd)
                fila1.adiciona(fregues)
                eventos.append(Evento(tempo_atual, id_proximo_fregues, TipoEvento.CHEGADA, 1))

Simulador().executar(1000, 1, 0.4)
