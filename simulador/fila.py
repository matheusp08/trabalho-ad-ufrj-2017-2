""" Modulo Fila
	 - Ordem de Atendimento: 'FCFS'
	 - Prioridade: 1,2..N
"""

class Fila:
    """ Classe principal da fila
    """

    def __init__(self, prioridade):
        self.prioridade = prioridade
        self.fregueses = []
        # Esperanças
        self.ns_med = 0
        self.nq_med = 0
        self.w_med = 0
        self.x_med = 0

        # Variancias:
        self.w_var = 0

    def adiciona(self, fregues):
        """ Metodo para adicionar fregueses na fila
        """
        self.fregueses.append(fregues)
