""" Modulo Fila
	 - Ordem de Atendimento: 'FCFS'
	 - Prioridade: 1,2..N
"""

def atualiza_esperanca(atual, fregueses, valor, fator):
    """ Metodo para atualizar a esperanca
        Args:
            atual: valor atual da esperanca a ser atualiza
            fregueses: lista com os fregueses
            valor: novo valor a ser adicionado para o calculo da media
            fator: variavel para saber se temos que somar ou subtrair a esperanca
                0 se for soma e -1 se for subtracao
    """
    n = len(fregueses)
    return (atual * (n - 1 - fator) + valor)/(n + fator) if (n + fator) != 0 else 0

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
            tambem atualiza a esperanca de Nq
        """
        # if fregues.prioridade == 1:
        #     print("Fregues %d chegou na fila %d no tempo %f" % (fregues.fregues_id, self.prioridade, fregues.tempo_chegada1))
        # else:
        #     print("Fregues %d chegou na fila %d no tempo %f" % (fregues.fregues_id, self.prioridade, fregues.tempo_chegada2))

        self.fregueses.append(fregues)
        self.nq_med = atualiza_esperanca(self.nq_med, self.fregueses, len(self.fregueses), 0)
    
    def remove(self):
        """ Metodo para remover o primeiro fregues da fila
        """
        # print("Fregues %d saiu na fila %d" % (self.fregueses[0].fregues_id, self.prioridade))
        self.fregueses = self.fregueses[1:]
        self.nq_med = atualiza_esperanca(self.nq_med, self.fregueses, -1, -1)

    def soma_servico_x(self, tempo):
        """ Metodo para atualizar a esperanca do servico X
        """
        self.x_med = atualiza_esperanca(self.x_med, self.fregueses, tempo, 0)

    def atualiza_tempo_w(self, valor):
        """ Metodo para atualizar a esperanca de W
        """
        self.w_med = atualiza_esperanca(self.w_med, self.fregueses, valor, 0)

    def atualiza_ns(self, valor):
        """ Metodo para atualizar a esperanca de Ns
        """
        self.ns_med = atualiza_esperanca(self.ns_med, self.fregueses, valor, 0)

    def tamanho(self):
        """ Metodo para retornar o tamanho da fila
        """
        return len(self.fregueses)

    def proximo_fregues(self):
        """ Metodo para retornar o primeiro fregues da fila
        """
        return self.fregueses[0]

    def imprime_esperancas(self):
        """ Metodo para imprimir as esperancas da fila
        """
        print("Fila %d" % self.prioridade)
        print("E[X]: %f" % self.x_med)
        print("E[W]: %f" % self.w_med)
        print("E[Nq]: %f" % self.nq_med)
        print("E[Ns]: %f" % self.ns_med)
        print("E[N]: %f" % (self.nq_med + self.ns_med))
        print("E[T]: %f" % (self.w_med + self.x_med))
        print("=======================")
