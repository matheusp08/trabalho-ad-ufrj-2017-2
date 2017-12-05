""" Modulo Evento
"""
from enum import Enum

class TipoEvento(Enum):
    """ Enum que define os tipos de eventos existentes
    """
    CHEGADA = "CHEGADA"
    FIM_SERVICO = "FIM_SERVICO"

class Evento:
    """ O evento tem os seguintes parametros:
            - Tempo que ocorreu
            - Id do fregues
            - Tipo de evento:
                - CHEGADA - Chegou no sistema (fila 1)
                - FIM_SERVICO
                    - - Se for da fila 1, indica a chegada na fila 2.
                    - - Se for da fila 2, indica a saída do sistema.
            - Prioridade
    """
    def __init__(self, tempo, fregues_id, tipo, prioridade):
        self.tempo = tempo
        self.fregues_id = fregues_id
        self.tipo = tipo
        self.prioridade = prioridade

        print("%d - %s FREGUES %d Fila %d" % (self.tempo, self.tipo.name, self.fregues_id, self.prioridade))
