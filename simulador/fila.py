""" Modulo Fila
	 - Ordem de Atendimento: 'FCFS'
	 - Prioridade: 1,2..N
"""

class Fila:
    """ Classe principal da fila
    """

    def __init__(self, prioridade, n_rodadas):
        self.prioridade = prioridade
        self.fregueses = []
        self.n_rodadas = n_rodadas
        # Esperanças
        self.ns_med = [0] * n_rodadas
        self.nq_med = [0] * n_rodadas
        self.w_med = [0] * n_rodadas
        self.x_med = [0] * n_rodadas

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

    def soma_servico_x(self, tempo, rodada):
        """ Funcao para somar o tempo do servico X
        """
        self.x_med[rodada] += tempo

    def soma_tempo_w(self, valor, rodada):
        """ Funcao para somar a esperanca de W
        """
        self.w_med[rodada] += valor

    def soma_nq(self, valor, rodada):
        """ Funcao para somar a esperanca de Nq
        """
        self.nq_med[rodada] += valor

    def soma_ns(self, valor, rodada):
        """ Funcao para somar a esperanca de Ns
        """
        self.ns_med[rodada] += valor

    def tamanho(self):
        """ Funcao para retornar o tamanho da fila
        """
        return len(self.fregueses)

    def proximo_fregues(self):
        """ Funcao para retornar o primeiro fregues da fila
        """
        return self.fregueses[0]

    def calcula_variancia_ns(self, valor, n, rodada):
        """ Metodo para calcular a variancia de Ns
        """
        return ((valor - (self.ns_med[rodada]/n))**2)/(n-1)

    def atualiza_esperancas(self, n_fregueses):
        """ Metodo para calcular de fato as esperancas
        """
        self.x_med = [x / n_fregueses for x in self.x_med]
        self.w_med = [w / n_fregueses for w in self.w_med]
        self.nq_med = [nq / n_fregueses for nq in self.nq_med]
        self.ns_med = [ns / n_fregueses for ns in self.ns_med]

    def imprime_esperancas(self):
        """ Funcao para imprimir as esperancas da fila
        """
        print("Fila %d" % self.prioridade)
        print("E[X]: %f" % self.x_med[self.n_rodadas-1])
        print("E[W]: %f" % self.w_med[self.n_rodadas-1])
        print("E[Nq]: %f" % self.nq_med[self.n_rodadas-1])
        print("E[Ns]: %f" % self.ns_med[self.n_rodadas-1])
        print("E[N]: %f" % (self.nq_med[self.n_rodadas-1] + self.ns_med[self.n_rodadas-1]))
        print("E[T]: %f" % (self.w_med[self.n_rodadas-1] + self.x_med[self.n_rodadas-1]))
        print("=======================")
