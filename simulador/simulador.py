"""Modulo Simulador


"""

from datetime import datetime
from matplotlib import pyplot as plt
from fila import Fila
from fregues import Fregues
from utils import Utils
from evento import Evento, TipoEvento
from plot import Plot

utilizacao = []

class Simulador:
    """Classe do simulador
    Attributes:
        taxa: taxa de entrada das filas
        t_student: distribuicao para intervalo de confianca de 95%
    """
    def __init__(self):
        self.t_student = Utils.get_distribuicao_t_student()

    def executar(self, n_fregueses, n_rodadas, rho):
        """ Funcao de execucao do simulador
        Args:
            n_fregueses: numero de fregueses
            n_rodadas: numero de rodadas da simulacao.
            rho: taxa
        """
        lambd = rho/2
        taxa_servico = 1
        resultados = []

        inicio = datetime.now()
        for i in range(n_rodadas):
            resultado = self.executar_rodada(n_fregueses, lambd, taxa_servico)
            resultados.append(resultado)
        fim = datetime.now()
        total = fim - inicio

        print("Tempo de execucao: " + str(total))

    def executar_rodada(self, n_fregueses, lambd, taxa_servico):
        """ Metodo responsavel pela execucao de cada rodada
        """
        global utilizacao
        fila1 = Fila(1)
        fila2 = Fila(2)
        eventos = []
        tempo = 0
        fregueses_servidos = 0
        id_proximo_fregues = 0
        fregues_executando = Fregues()
        

        while fregueses_servidos < n_fregueses:
            tempo_ate_prox_chegada = Utils.gera_taxa_exp_seed(lambd)
            tempo += tempo_ate_prox_chegada

            while tempo_ate_prox_chegada > 0 and fregues_executando.fregues_id != -1:
                if fregues_executando.tempo_restante < tempo_ate_prox_chegada:
                    tempo_ate_prox_chegada -= fregues_executando.tempo_restante
                    fregues_executando.tempo_restante = 0
                    tempo_atual = tempo - tempo_ate_prox_chegada
                    eventos.append(
                        Evento(tempo_atual,
                            fregues_executando.fregues_id,
                            TipoEvento.FIM_SERVICO,
                            fregues_executando.prioridade))
                    
                    if fregues_executando.prioridade == 1:
                        w1 = tempo_atual - fregues_executando.tempo_chegada1 - fregues_executando.tempo_servico1
                        fila1.atualiza_tempo_w(w1)
                        fila1.remove()
                        fregues_executando.troca_fila(tempo_atual)
                        fila2.adiciona(fregues_executando)
                        eventos.append(Evento(tempo_atual, fregues_executando.fregues_id, TipoEvento.CHEGADA, 2))
                    else:
                        w2 = tempo_atual - fregues_executando.tempo_chegada2 - fregues_executando.tempo_servico2
                        fila2.atualiza_tempo_w(w2)
                        fila2.remove()
                        fregueses_servidos += 1
                    
                    if fila1.tamanho() > 0:
                        fregues_executando = fila1.proximo_fregues()
                    else:
                        if fila2.tamanho() > 0:
                            fregues_executando = fila2.proximo_fregues()
                        else:
                            fregues_executando = Fregues()
                else:
                    fregues_executando.tempo_restante -= tempo_ate_prox_chegada
                    tempo_ate_prox_chegada = 0

            if id_proximo_fregues < n_fregueses:
                fregues = Fregues(id_proximo_fregues, tempo, taxa_servico)
                fila1.soma_servico_x(fregues.tempo_servico1)
                fila2.soma_servico_x(fregues.tempo_servico2)

                fila1.atualiza_nq(fila1.tamanho())
                fila2.atualiza_nq(fila2.tamanho())

                fila1.adiciona(fregues)
                eventos.append(Evento(tempo, id_proximo_fregues, TipoEvento.CHEGADA, 1))
                if fregues_executando.fregues_id == -1:
                    fregues_executando = fregues
                else:
                    if fregues_executando.prioridade == 2:
                        fregues_executando = fregues
                        fila2.atualiza_nq(-1)
                        fila2.atualiza_ns(1)
                    else:
                        fila1.atualiza_nq(-1)
                        fila1.atualiza_ns(1)
                id_proximo_fregues += 1
                
            if id_proximo_fregues % 10 == 0:
                utilizacao.append((fila1.ns_med + fila2.ns_med)/id_proximo_fregues)

        fila1.atualiza_esperancas(n_fregueses)
        fila2.atualiza_esperancas(n_fregueses)
        fila1.imprime_esperancas()
        fila2.imprime_esperancas()

Simulador().executar(10000, 1, 0.4)
Plot().desenha_grafico(utilizacao, 'Numero de Fregueses', 'Utilizacao do Servidor')
