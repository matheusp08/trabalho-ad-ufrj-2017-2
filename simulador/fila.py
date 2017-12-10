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

    def adiciona(self, fregues):
        """ Funcao para adicionar fregueses na fila
        """
        self.fregueses.append(fregues)

    def volta_para_fila(self, fregues):
        """ Funcao para voltar um fregues para o inicio da fila
        """
        self.fregueses = [fregues] + self.fregueses

    def tamanho(self):
        """ Funcao para retornar o tamanho da fila
        """
        return len(self.fregueses)

    def proximo_fregues(self):
        """ Funcao para retornar o primeiro fregues da fila, removendo-o da mesma
        """
        return self.fregueses.pop(0)
