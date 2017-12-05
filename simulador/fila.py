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

    def adiciona(self, fregues):
        """ Funcao para adicionar fregueses na fila
        """
        self.fregueses.append(fregues)
    
    def volta_para_fila(self, fregues):
        """ Funcao para voltar um fregues para o inicio da fila
        """
        self.fregueses = [fregues] + self.fregueses

    def remove(self):
        """ Funcao para remover o primeiro fregues da fila
        """
        self.fregueses = self.fregueses[1:]

    def soma_servico_x(self, tempo):
        """ Funcao para somar o tempo do servico X
        """
        self.x_med += tempo

    def soma_tempo_w(self, valor):
        """ Funcao para somar a esperanca de W
        """
        self.w_med += valor

    def soma_nq(self, valor):
        """ Funcao para somar a esperanca de Nq
        """
        self.nq_med += valor

    def soma_ns(self, valor):
        """ Funcao para somar a esperanca de Ns
        """
        self.ns_med += valor

    def tamanho(self):
        """ Funcao para retornar o tamanho da fila
        """
        return len(self.fregueses)

    def proximo_fregues(self):
        """ Funcao para retornar o primeiro fregues da fila
        """
        return self.fregueses[0]

    def calcula_variancia_ns(self, valor, n):
        """ Metodo para calcular a variancia de Ns
        """
        return ((valor - (self.ns_med/n))**2)/(n-1)

    def atualiza_esperancas(self, n_fregueses):
        """ Metodo para calcular de fato as esperancas
        """
        self.x_med /= n_fregueses
        self.w_med /= n_fregueses
        self.nq_med /= n_fregueses
        self.ns_med /= n_fregueses

    def imprime_esperancas(self):
        """ Funcao para imprimir as esperancas da fila
        """
        print("Fila %d" % self.prioridade)
        print("E[X]: %f" % self.x_med)
        print("E[W]: %f" % self.w_med)
        print("E[Nq]: %f" % self.nq_med)
        print("E[Ns]: %f" % self.ns_med)
        print("E[N]: %f" % (self.nq_med + self.ns_med))
        print("E[T]: %f" % (self.w_med + self.x_med))
        print("=======================")
