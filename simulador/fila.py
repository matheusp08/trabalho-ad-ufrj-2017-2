""" Modulo Fila
	A fila recebe os 4 parâmetros descritos abaixo:
	 - Ordem de Atendimento: 'LCFS', 'FCFS'
	 - Prioridade: 1,2..N
	 - Taxa de Entrada: Lambda
	 - Taxa de Serviço: mi
"""

class Fila:
    """ Classe principal da fila
    """
    # Esperanças
    N = 0
    Nq = 0
    W = 0
    X = 0

    # Variancias:
    varW = 0

    def __init__(self, tipo, prioridade, taxa_chegada):
        self.tipo = tipo
        self.prioridade = prioridade
        self.taxa_chegada = taxa_chegada

    def imprime_parametros(self):
        """Funcao para imprimir os parametros da fila
            Args:
                Nenhum argumento
            Returns:
                Nenhum retorno
        """
        print("Fila %d" % self.prioridade)
        print("Tipo da fila: %s" % self.tipo)
        print("Prioridade: %d" % self.prioridade)
        print("Taxa de chegada: %f" % self.taxa_chegada)
