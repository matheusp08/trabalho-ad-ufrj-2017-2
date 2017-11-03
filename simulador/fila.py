"""A fila recebe os 4 parametros descritos abaixo:
    - Ordem de atendimento: 'FCFS', 'LCFS'
    - Prioridade: 1, 2,..., N
    - Taxa de entrada
"""

class Fila:
    """Classe que representa as filas do sistema
        Args:
            tipo (str): Tipo da fila
            prioridade (int): Prioridade da fila
            taxa_entrada (int): Taxa de entrada da fila

        Attributes:
            tipo (str): Tipo da fila
            prioridade (int): Prioridade da fila
            taxa_entrada (int): Taxa de entrada da fila
    """
    def __init__(self, tipo, prioridade, taxa_entrada):
        self.tipo = tipo
        self.prioridade = prioridade
        self.taxa_entrada = taxa_entrada
        self.imprime_parametros()

    def imprime_parametros(self):
        """Funcao para imprimir os parametros da fila
            Args:
                Nenhum argumento
            Returns:
                Nenhum retorno
        """
        print("Tipo da fila: %s" % self.tipo)
        print("Prioridade: %d" % self.prioridade)
        print("Taxa de entrada: %f" % self.taxa_entrada)
