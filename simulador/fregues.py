""" Modulo Fregues
"""

from utils import Utils

class Fregues:
    """ Classe que representa os fregueses do sistema
    """

    def __init__(self, fregues_id, tempo_chegada, taxa_servico):
        self.fregues_id = fregues_id
        self.tempo_chegada1 = tempo_chegada
        self.tempo_chegada2 = 0
        self.tempo_servico1 = Utils.gera_taxa_exp_seed(taxa_servico)
        self.tempo_servico2 = Utils.gera_taxa_exp_seed(taxa_servico)
        self.tempo_restante = self.tempo_servico1
        self.prioridade = 1
