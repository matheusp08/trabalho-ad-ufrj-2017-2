"""Modulo Simulador
"""
from datetime import datetime
from matplotlib import pyplot as plt
import sys
from fila import Fila
from fregues import Fregues
from utils import Utils
from evento import Evento, TipoEvento
from plot import Plot

utilizacao = []
variancia_ns = []

class Simulador:
    """Classe do simulador
    Attributes:
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

        inicio = datetime.now()
        self.executar_rodadas(n_rodadas, n_fregueses, lambd, taxa_servico)
        fim = datetime.now()
        total = fim - inicio

        print("Tempo de execucao: " + str(total))

    def executar_rodadas(self, n_rodadas, n_fregueses, lambd, taxa_servico):
        """ Metodo responsavel pela execucao de cada rodada
        """
        global utilizacao
        global variancia_ns
        fila1 = Fila(1, n_rodadas)
        fila2 = Fila(2, n_rodadas) 
        tempo = 0
        id_proximo_fregues = 0
        fregueses_servidos = 0
        rodada_atual = 0
        eventos = []
        fregues_executando = Fregues()

        # utilizacao = [[] for _ in range(n_rodadas)]

        while rodada_atual < n_rodadas:
            tempo_ate_prox_chegada = Utils.gera_taxa_exp_seed(lambd)
            tempo += tempo_ate_prox_chegada

            while tempo_ate_prox_chegada > 0 and fregues_executando.fregues_id != -1:
                if fregues_executando.tempo_restante <= tempo_ate_prox_chegada:
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
                        fila1.soma_tempo_w(w1, rodada_atual)
                        fila1.remove()
                        fregues_executando.troca_fila(tempo_atual)
                        fila2.adiciona(fregues_executando)
                        eventos.append(Evento(tempo_atual, fregues_executando.fregues_id, TipoEvento.CHEGADA, 2))
                    else:
                        w2 = tempo_atual - fregues_executando.tempo_chegada2 - fregues_executando.tempo_servico2
                        fila2.soma_tempo_w(w2, rodada_atual)
                        fila2.remove()
                        fregueses_servidos += 1
                        if fregueses_servidos % n_fregueses == 0:
                            fregueses_servidos = 0
                            rodada_atual += 1
                            if rodada_atual < n_rodadas:
                                fila1.ns_med[rodada_atual] += fila1.ns_med[rodada_atual-1]
                                fila2.ns_med[rodada_atual] += fila2.ns_med[rodada_atual-1]
                    
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

            if (id_proximo_fregues == n_fregueses * n_rodadas):
                break

            fregues = Fregues(id_proximo_fregues, tempo, taxa_servico, rodada_atual)
            fila1.soma_servico_x(fregues.tempo_servico1, rodada_atual)
            fila2.soma_servico_x(fregues.tempo_servico2, rodada_atual)

            fila1.soma_nq(fila1.tamanho(), rodada_atual)
            fila2.soma_nq(fila2.tamanho(), rodada_atual)

            fila1.adiciona(fregues)
            eventos.append(Evento(tempo, id_proximo_fregues, TipoEvento.CHEGADA, 1))
            if fregues_executando.fregues_id == -1:
                fregues_executando = fregues
            else:
                if fregues_executando.prioridade == 2:
                    fregues_executando = fregues
                    fila2.soma_nq(-1, rodada_atual)
                    fila2.soma_ns(1, rodada_atual)
                else:
                    fila1.soma_nq(-1, rodada_atual)
                    fila1.soma_ns(1, rodada_atual)
            id_proximo_fregues += 1

            # o calculo da varianca de Ns da fila 1 nos permite calcular uma possivel fase transiente
            # if id_proximo_fregues % 10 == 0:
            if id_proximo_fregues > 1:
                # variancia_ns.append(fila1.calcula_variancia_ns(1, id_proximo_fregues, rodada_atual))
                media = (fila1.ns_med[rodada_atual] + fila2.ns_med[rodada_atual])/id_proximo_fregues
                utilizacao.append(media)

        fila1.atualiza_esperancas(n_fregueses)
        fila2.atualiza_esperancas(n_fregueses)
        fila1.imprime_esperancas()
        fila2.imprime_esperancas()


def main(argv):

    if(len(sys.argv) < 4):
        print("Rode com os seguintes parametros: python3 simulador.py numero_rodadas fregueses_por_rodada rho")
        sys.exit()
    NUMERO_RODADAS = int(sys.argv[1])
    FREGUESES_POR_RODADAS = int(sys.argv[2])
    RHO = float(sys.argv[3])

    Simulador().executar(FREGUESES_POR_RODADAS, NUMERO_RODADAS, RHO)
    Plot().desenha_grafico(utilizacao, 'Numero de Fregueses', 'Utilizacao do Servidor', FREGUESES_POR_RODADAS*NUMERO_RODADAS)
    # Plot().desenha_grafico(utilizacao[1], 'Numero de Fregueses', 'Utilizacao do Servidor', 10000)
    # Plot().desenha_grafico(variancia_ns, 'Numero de Fregueses', 'Variancia de Ns', 10000)


if __name__ == "__main__": main(sys.argv)