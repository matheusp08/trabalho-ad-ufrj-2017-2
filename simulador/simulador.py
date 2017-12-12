"""Modulo Simulador
"""
import sys
from datetime import datetime
from fila import Fila
from fregues import Fregues
from utils import Utils
# from evento import Evento, TipoEvento
from metrica import Metrica
from plot import Plot
from prettytable import PrettyTable

class Simulador:
    def executar(self, n_rodadas, fregueses_por_rodada, rho, n_transiente):
        """ Funcao de execucao do simulador
        Args:
            n_fregueses: numero de fregueses
            n_rodadas: numero de rodadas da simulacao.
            rho: taxa
        """

        ''' Inicializacao '''
        lambd = rho/2                   # taxa de chegada.
        taxa_servico = 1                # taxa de servico.
        
        fila1 = Fila(1)                 # fila 1, mais prioritaria (chegadas exogenas).
        fila2 = Fila(2)                 # fila 2, menos prioritaria (nao ha chagadas exogenas).
        # eventos = []                    # lista de eventos.

        total_fregueses_servidos = 0    # total de fregueses que passaram pelo sistema.
        total_fregueses_criados = 0     # total de fregueses criados pelo sistema
        tempo = 0                       # tempo atual da simulacao.
        rodada_atual = 0                # rodada da fase transiente.
        fregues_executando = None       # inicializacao nula do fregues executando.

        plot = Plot()
        intervalo = (n_transiente + (fregueses_por_rodada * n_rodadas)) * 0.1
        metricas = Metrica(n_rodadas, fregueses_por_rodada) 
        if n_transiente > 0:
            id_proximo_fregues = - n_transiente
        else:
            id_proximo_fregues = 0   # id do proximo fregues a ser criado (fase transiente arbitraria)


        ''' Casos DETERMINISTICOS '''
        deterministico = False
        xs1 = [0]      
        xs2 = [0]
        if deterministico:              # Caso de Interrupcao.
            chegadas = [1, 4]           # Os vetores representam caracteristicas de todos os fregueses.
            xs1 = [1, 2]                
            xs2 = [5, 2]                   
            # chegadas = [0, 4]         # Caso de Servidor Ocioso.
            # xs1 = [1, 1]
            # xs2 = [1, 2]   
            

        ''' Execucao da SIMULACAO '''
        inicio = datetime.now()
        while total_fregueses_servidos < n_rodadas * fregueses_por_rodada:  # Loop de execucao sobre as RODADAS.
            
            # Tempo de chegada conforme sistema Deterministico:
            if deterministico:
                if len(chegadas) > 0:
                    tempo_ate_prox_chegada = chegadas.pop(0)-tempo
                else:
                    tempo_ate_prox_chegada = 10
            # Tempo de chegada conforme sistema Exponencial:
            else:
                tempo_ate_prox_chegada = Utils.gera_taxa_exp(lambd)  
            tempo += tempo_ate_prox_chegada


            # Loop de execucao enquanto ainda nao chegar um novo fregues
            while tempo_ate_prox_chegada > 0 and fregues_executando is not None:    
                
                # Se a execucao do fregues acabar antes da proxima chegada.
                if fregues_executando.tempo_restante <= tempo_ate_prox_chegada:     
                    tempo_ate_prox_chegada -= fregues_executando.tempo_restante     # O tempo ate a prox chegada sera subtraido do tempo de servico do fregues em execucao
                    fregues_executando.tempo_restante = 0
                    tempo_atual = tempo - tempo_ate_prox_chegada
                    cor = fregues_executando.cor
                    # eventos.append(Evento(tempo_atual, fregues_executando.fregues_id, TipoEvento.FIM_SERVICO, fregues_executando.prioridade))
                    
                    # Atualizacao de metricas de acordo com a fila do fregues (1 ou 2).
                    # E realizacao da troca de filas (para o fregues que executou em 1) ou evento de fim de execucao (fregues dafila 2)
                    if fregues_executando.prioridade == 1:
                        w1 = tempo_atual - fregues_executando.tempo_chegada1 - fregues_executando.tempo_servico1
                        if cor <= n_rodadas: # so calcula metricas dos fregueses ate n_rodadas
                            metricas.acumula_w1(w1, cor)
                            plot.w1_acumulado += w1
                            metricas.acumula_t1(w1, cor)
                        fregues_executando.troca_fila(tempo_atual)
                        fila2.adiciona(fregues_executando)
                        # eventos.append(Evento(tempo_atual, fregues_executando.fregues_id, TipoEvento.CHEGADA, 2))
                    else:
                        w2 = tempo_atual - fregues_executando.tempo_chegada2 - fregues_executando.tempo_servico2
                        if cor <= n_rodadas: # so calcula metricas dos fregueses ate n_rodadas
                            metricas.acumula_w2(w2, cor)
                            plot.w2_acumulado += w2
                            metricas.acumula_t2(w2, cor)
                        # if para garantir que os fregueses das rodadas foram os servidos
                        if fregues_executando.cor > 0 and fregues_executando.cor <= n_rodadas:
                            total_fregueses_servidos += 1

                    # Caso exista freguese na fila: coloca-lo em execucao (Prioridade para fila 1).
                    if fila1.tamanho() > 0:
                        fregues_executando = fila1.proximo_fregues()
                    else:
                        if fila2.tamanho() > 0:
                            fregues_executando = fila2.proximo_fregues()
                        else:
                            fregues_executando = None
                
                # Caso chegue um outro fregues no meio da execucao do fregues atual.
                else:
                    fregues_executando.tempo_restante -= tempo_ate_prox_chegada
                    tempo_ate_prox_chegada = 0


            # Tratando as rodadas.
            if id_proximo_fregues >= 0 and id_proximo_fregues % fregueses_por_rodada == 0:
                rodada_atual += 1

            if deterministico and total_fregueses_servidos == fregueses_por_rodada:
                break
            # Chega um novo fregues: entra na fila 1.
            fregues = Fregues(id_proximo_fregues, tempo, taxa_servico, rodada_atual, xs1[0], xs2[0])
            if deterministico:
                del xs1[0]
                del xs2[0]
            
            # Atualizacao de Metricas.
            if rodada_atual <= n_rodadas:
                metricas.acumula_x1(fregues.tempo_servico1, rodada_atual)
                metricas.acumula_t1(fregues.tempo_servico1, rodada_atual)
                metricas.acumula_nq1(fila1.tamanho(), rodada_atual)
                metricas.acumula_n1(fila1.tamanho(), rodada_atual)
                metricas.acumula_x2(fregues.tempo_servico2, rodada_atual)
                metricas.acumula_t2(fregues.tempo_servico2, rodada_atual)
                metricas.acumula_nq2(fila2.tamanho(), rodada_atual)
                metricas.acumula_n2(fila2.tamanho(), rodada_atual)
                plot.nq1_acumulado += fila1.tamanho()
                plot.nq2_acumulado += fila2.tamanho()

            # eventos.append(Evento(tempo, id_proximo_fregues, TipoEvento.CHEGADA, 1))

            # Rotina de verificacao de quem deve executar.
            if fregues_executando is None:
                fregues_executando = fregues
            else:                                               # Interrupcao, Novo fregues executa.
                if fregues_executando.prioridade == 2:
                    fila2.volta_para_fila(fregues_executando)
                    fregues_executando = fregues
                    if rodada_atual <= n_rodadas:
                        metricas.acumula_ns2(1, rodada_atual)
                        plot.ns2_acumulado += 1
                        metricas.acumula_n2(1, rodada_atual)
                else:                                           # Novo fregues para fila 1.
                    fila1.adiciona(fregues)
                    if rodada_atual <= n_rodadas:
                        metricas.acumula_ns1(1, rodada_atual)
                        plot.ns1_acumulado += 1
                        metricas.acumula_n1(1, rodada_atual)
            id_proximo_fregues += 1
            total_fregueses_criados += 1

            # if id_proximo_fregues % intervalo == 0:
            plot.w1.append(plot.w1_acumulado / total_fregueses_criados)
            plot.nq1.append(plot.nq1_acumulado / total_fregueses_criados)
            plot.ns1.append(plot.ns1_acumulado / total_fregueses_criados)
            plot.w2.append(plot.w2_acumulado / total_fregueses_criados)
            plot.nq2.append(plot.nq2_acumulado / total_fregueses_criados)
            plot.ns2.append(plot.ns2_acumulado / total_fregueses_criados)

        # Impressao dos parametros de entrada.
        tabela_parametros = PrettyTable(["n_rodadas", "fregueses/rodada", "fase_transiente", "rho", "lambda"])
        tabela_parametros.add_row([n_rodadas, fregueses_por_rodada, n_transiente, rho, lambd])
        print(tabela_parametros, "\n")

        # Calculo e impressao das metricas.
        metricas.calcula(deterministico)

        fim = datetime.now()
        total = fim - inicio
        print("Tempo de execucao: " + str(total))

        # plota os graficos
        plot.desenha(intervalo, n_rodadas, fregueses_por_rodada, n_transiente, rho)

def main(argv):
    """ Funcao main
    """
    if len(argv) < 5:
        print("Execucao deve ser: python3 simulador.py numero_rodadas fregueses_por_rodada fase_transiente rho")
        sys.exit()

    n_rodadas = int(argv[1])
    fregueses_por_rodada = int(argv[2])
    n_transiente = int(argv[3])
    rho = float(argv[4])

    Simulador().executar(n_rodadas, fregueses_por_rodada, rho, n_transiente)

if __name__ == "__main__":
    main(sys.argv)
