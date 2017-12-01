""" Modulo Fregues
"""

from utils import Utils

class Fregues:
    """ Classe que representa os fregueses do sistema
    """

    def __init__(self, fregues_id = -1, tempo_chegada = -1, taxa_servico = -1, cor = 0):
        self.fregues_id = fregues_id
        self.tempo_chegada1 = tempo_chegada
        self.tempo_chegada2 = 0
        self.tempo_servico1 = Utils.gera_taxa_exp_seed(taxa_servico)
        self.tempo_servico2 = Utils.gera_taxa_exp_seed(taxa_servico)
        self.tempo_restante = self.tempo_servico1
        self.prioridade = 1
        self.cor = cor

    def troca_fila(self, tempo):
        """ Funcao para mudar o fregues para a chegada na fila 2
        """
        self.prioridade = 2
        self.tempo_chegada2 = tempo
        self.tempo_restante = self.tempo_servico2