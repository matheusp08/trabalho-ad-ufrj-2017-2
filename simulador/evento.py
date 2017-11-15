""" Modulo principal dos Eventos
	Um evento, que pode ser chegada, fim de serviço, etc.
	O evento tem os seguintes parâmetros:
	 - Tempo de Chegada
	 - Número do freguês
	 - Tipo de evento:
		- Chegou no sistema (= chegada fila 1)
    	- Fim servico 1
			- Se for da fila 1, indica a chegada na fila 2.
		- Fim servico 2
            - Se for da fila 2, indica a saída do sistema.
	- Prioridade
"""
from enum import Enum

class TipoEvento(Enum):
    """ Enum que define os tipos de eventos existentes
    """
    CHEGADA = "CHEGADA"
    FIM_SERVICO = "FIM_SERVICO"

class Evento:
    """ Classe principal dos eventos do sistema
    """
    def __init__(self, tempo, fregues_id, tipo, prioridade):
        self.tempo = tempo
        self.fregues_id = fregues_id
        self.tipo = tipo
        self.prioridade = prioridade

        # print("Evento de %s ocorreu no tempo %f pelo fregues %d de prioridade %d" % (self.tipo.name, self.tempo, self.fregues_id, self.prioridade))
