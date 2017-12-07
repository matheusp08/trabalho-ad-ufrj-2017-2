"""Modulo Simulador
"""
import sys
from datetime import datetime
from fila import Fila
from fregues import Fregues
from utils import Utils
from evento import Evento, TipoEvento
from plot import Plot

UTILIZACAO = []
VARIANCIA_NS = []

class Simulador:
    """Classe do simulador
    Attributes:
    """
    def executar(self, n_rodadas, fregueses_por_rodada, rho, n_transiente):
        """ Funcao de execucao do simulador
        Args:
            n_fregueses: numero de fregueses
            n_rodadas: numero de rodadas da simulacao.
            rho: taxa
        """
        global UTILIZACAO
        global VARIANCIA_NS

        lambd = rho/2                    # taxa de chegada
        taxa_servico = 1                 # taxa de servico

        fila1 = Fila(1, n_rodadas)       # fila 1, mais prioritaria (chegadas exogenas)
        fila2 = Fila(2, n_rodadas)       # fila 2, menos prioritaria (nao ha chagadas exogenas)
        eventos = []                     # lista de eventos

        tempo = 0                        # tempo atual da simulacao
        fregues_executando = None        # inicializacao nula do fregues executando
        total_fregueses_servidos = 0     # total de fregueses que passaram pelo sistema
        fregueses_criados = 0            # total de fregueses criados na simulacao
        
        rodada_atual = 0                     # rodada da fase transiente
        
        if n_transiente > 0:
            id_proximo_fregues = -n_transiente   # id do proximo fregues a ser criado (fase transiente arbitraria)
        else:
            id_proximo_fregues = 0               # id do proximo fregues a ser criado 

        inicio = datetime.now()          # tempo inicial de execucao da simulacao para calculo posterior
        
        # enquanto nao foram executadas n rodadas, conforme parametro de entrada, o programa permanece no loop abaixo
        while total_fregueses_servidos < n_rodadas * fregueses_por_rodada:
            # eh gerado o tempo ate a chegada de um proximo fregues usando a taxa de chegada lambd
            tempo_ate_prox_chegada = Utils.gera_taxa_exp_seed(lambd)
            # e com isso, o tempo do sistema eh somado do tempo que o proximo fregues chegara
            tempo += tempo_ate_prox_chegada

            # se ainda tiver tempo livre ate a proxima chegada e algum fregues tiver executando, tratamos a sua execucao
            while tempo_ate_prox_chegada > 0 and fregues_executando is not None:
                # se o tempo restante de servico do fregues em execucao for menor do que a proxima chegada, tratamos sua execucao abaixo
                if fregues_executando.tempo_restante <= tempo_ate_prox_chegada:
                    # subtraimos do tempo ate a chegada do proximo fregues do tempo que o fregues que estava executando utilizou
                    tempo_ate_prox_chegada -= fregues_executando.tempo_restante
                    fregues_executando.tempo_restante = 0
                    tempo_atual = tempo - tempo_ate_prox_chegada
                    cor = fregues_executando.cor
                    # geramos um evento de fim de servico
                    eventos.append(
                        Evento(tempo_atual,
                            fregues_executando.fregues_id,
                            TipoEvento.FIM_SERVICO,
                            fregues_executando.prioridade))
                    # e agora verificamos se o fregues que estava executando era da fila 1, se sim, atualizamos a metrica W1, 
                    # removemos ele da fila 1 e adicionamos na fila 2, gerando um evento de chegada 2
                    if fregues_executando.prioridade == 1:
                        w1 = tempo_atual - fregues_executando.tempo_chegada1 - fregues_executando.tempo_servico1
                        fila1.soma_tempo_w(w1, cor)
                        fregues_executando.troca_fila(tempo_atual)
                        fila2.adiciona(fregues_executando)
                        eventos.append(Evento(tempo_atual, fregues_executando.fregues_id, TipoEvento.CHEGADA, 2))
                    # se o fregues que terminou de executar era da fila 2, basta atualizarmos a metrica W2 e removermos ele da fila 2,
                    # pois o mesmo agora saira do sistema, terminando sua execucao
                    else:
                        w2 = tempo_atual - fregues_executando.tempo_chegada2 - fregues_executando.tempo_servico2
                        fila2.soma_tempo_w(w2, cor)
                        if fregues_executando.cor > 0:
                            total_fregueses_servidos += 1
                    
                    # agora temos que colocar alguem em execucao se alguma das filas nao estiver vazia, lembrando que a prioridade
                    # eh sempre da fila 1
                    if fila1.tamanho() > 0:
                        fregues_executando = fila1.proximo_fregues()
                    else:
                        if fila2.tamanho() > 0:
                            fregues_executando = fila2.proximo_fregues()
                        else:
                            fregues_executando = None
                # como o tempo restente para a execucao eh maior do que o tempo ate a chegada de um proximo fregues, temos que tratar primeiro
                # a chegada, pois ela influencia nas metricas
                else:
                    fregues_executando.tempo_restante -= tempo_ate_prox_chegada
                    tempo_ate_prox_chegada = 0

            if id_proximo_fregues % fregueses_por_rodada == 0:
                rodada_atual += 1            

            if rodada_atual > n_rodadas:
                break

            # agora tratamos a chegada de um novo fregues, criando um novo objeto Fregues, adicionando-o na fila 1, lancando um
            # evento de chegada 1 e atualizando as metricas X1, X2, Nq1 e Nq2
            fregues = Fregues(id_proximo_fregues, tempo, taxa_servico, rodada_atual)
            fila1.soma_servico_x(fregues.tempo_servico1, rodada_atual)
            fila2.soma_servico_x(fregues.tempo_servico2, rodada_atual)

            fila1.soma_nq(fila1.tamanho(), rodada_atual)
            fila2.soma_nq(fila2.tamanho(), rodada_atual)

            eventos.append(Evento(tempo, id_proximo_fregues, TipoEvento.CHEGADA, 1))

            # se nao tem ninguem executando, esse fregues ja vai ser servido diretamente
            if fregues_executando is None:
                fregues_executando = fregues
            else:
                # se existe algum fregues de prioridade 2 executando, esse novo fregues tera a prioridade de execucao
                if fregues_executando.prioridade == 2:
                    fila2.volta_para_fila(fregues_executando)
                    fregues_executando = fregues
                    fila2.soma_ns(1, rodada_atual)
                # se existe algum fregues de prioridade 1 executando, o novo fregues eh somente adicionado na fila 1
                else:
                    fila1.adiciona(fregues)
                    fila1.soma_ns(1, rodada_atual)
            # o id do proximo fregues eh entao acrescido de 1
            id_proximo_fregues += 1
            fregueses_criados += 1
            
            # calculamos a variancia da utilizacao do sistema para talvez utilizar para achar a fase transiente
            # if fregueses_criados % 10 == 0:
            #     # VARIANCIA_NS.append(fila1.calcula_variancia_ns(1, id_proximo_fregues, rodada_atual))
            #     media = (fila1.ns_med[rodada_atual] + fila2.ns_med[rodada_atual])/fregueses_criados
            #     UTILIZACAO.append(media)

        #atualizamos as esperancas acumuladas durante a simulacao
        fila1.atualiza_esperancas(fregueses_por_rodada)
        fila2.atualiza_esperancas(fregueses_por_rodada)
        fila1.imprime_esperancas()
        fila2.imprime_esperancas()

        # e por fim, calculamos o tempo total da simulacao
        fim = datetime.now()
        total = fim - inicio
        print("Tempo de execucao: " + str(total))

def main(argv):
    """ Funcao main
    """

    if len(argv) < 4:
        print("Execucao deve ser: python3 simulador.py numero_rodadas fregueses_por_rodada rho")
        sys.exit()

    n_rodadas = int(argv[1])
    fregueses_por_rodada = int(argv[2])
    rho = float(argv[3])
    n_transiente = 5000

    Simulador().executar(n_rodadas, fregueses_por_rodada, rho, n_transiente)
    # Plot().desenha_grafico(UTILIZACAO, 'Numero de Fregueses', 'Utilizacao do Servidor', fregueses_por_rodada*n_rodadas)
    # Plot().desenha_grafico(utilizacao[1], 'Numero de Fregueses', 'Utilizacao do Servidor', 10000)
    # Plot().desenha_grafico(variancia_ns, 'Numero de Fregueses', 'Variancia de Ns', 10000)

if __name__ == "__main__":
    main(sys.argv)
