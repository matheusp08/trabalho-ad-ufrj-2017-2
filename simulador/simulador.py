""" Modulo Simulador
"""
from datetime import datetime
from matplotlib import pyplot as plt
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
        fila1 = Fila(1)
        fila2 = Fila(2) 
        tempo = 0
        id_proximo_fregues = 0
        fregueses_servidos = 0
        rodada_atual = 1
        eventos = []
        fregues_executando = Fregues()
        nao_tem_mais_ngm_p_chegar = 0
        executando = ""
        
        
        while fregueses_servidos < n_fregueses:
            tempo_ate_prox_chegada = lambd
            tempo += tempo_ate_prox_chegada
            print("\nTEMPO DE EXECUÇÃO: ", tempo)

            if id_proximo_fregues < n_fregueses:
                # Pq diabos esse comeco estava fora desse if? Acaba nao tratando o caso em que tempo_restante = tempo_ate_prox_chegada !!
                print("[New Fregues] ID:", id_proximo_fregues)
                fregues = Fregues(id_proximo_fregues, tempo, taxa_servico, rodada_atual)
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
                    #if fregues.prioridade == 1:
                    #   print("Fregues", fregues_executando.fregues_id, "(fila", fregues_executando.prioridade,") foi interrompido pelo fregues", fregues.fregues_id, "(fila", fregues.prioridade,")")
                    if fregues_executando.tempo_restante != 0:
                        fregues_executando = fregues
                    fila2.atualiza_nq(-1)
                    fila2.atualiza_ns(1)
                else:
                    fila1.atualiza_nq(-1)
                    fila1.atualiza_ns(1)
            if id_proximo_fregues < n_fregueses:        
                id_proximo_fregues += 1
            else:
                nao_tem_mais_ngm_p_chegar = 1
            
            while (tempo_ate_prox_chegada > 0 and fregues_executando.fregues_id != -1) or nao_tem_mais_ngm_p_chegar:
                # print("While 2. Tempo: ", tempo, ". Tempo restante: ", fregues_executando.tempo_restante, ". PRox chegada: ", tempo_ate_prox_chegada);
                if fregues_executando.tempo_restante > 0:
                    executando = "   - EXECUTANDO"
                else:
                    executando = " - ACABOU"
                print("[Tempo Restante] Fregues:", fregues_executando.fregues_id, ", Tempo: ", fregues_executando.tempo_restante, executando)
                
                
                if (fregues_executando.tempo_restante < tempo_ate_prox_chegada) or nao_tem_mais_ngm_p_chegar:
                    tempo_ate_prox_chegada -= fregues_executando.tempo_restante
                    if nao_tem_mais_ngm_p_chegar:
                        tempo = tempo + fregues_executando.tempo_restante
                        #print("\nTEMPO DE EXECUÇÃO: ", tempo)
                    fregues_executando.tempo_restante = 0
                    ##Acho que posso printar o tempo aqui!!!
                    tempo_atual = tempo - tempo_ate_prox_chegada
                    eventos.append(
                        Evento(tempo_atual,
                            fregues_executando.fregues_id,
                            TipoEvento.FIM_SERVICO,
                            fregues_executando.prioridade))
                    
                    if fregues_executando.prioridade == 1:
                        #print("\nTEMPO DE EXECUÇÃO: ", tempo + 1)
                        print("[Mudando de Fila] Fregues", fregues_executando.fregues_id)
                        w1 = tempo_atual - fregues_executando.tempo_chegada1 - fregues_executando.tempo_servico1
                        fila1.atualiza_tempo_w(w1)
                        fila1.remove()
                        fregues_executando.troca_fila(tempo_atual)
                        fila2.adiciona(fregues_executando)
                        eventos.append(Evento(tempo_atual, fregues_executando.fregues_id, TipoEvento.CHEGADA, 2))
                    else:
                        print("Fregues", fregues_executando.fregues_id , "indo embora..")
                        w2 = tempo_atual - fregues_executando.tempo_chegada2 - fregues_executando.tempo_servico2
                        fila2.atualiza_tempo_w(w2)
                        fila2.remove()
                        fregueses_servidos += 1
                        if fregueses_servidos == n_fregueses:
                            print("ACABARAM TODOS OS FREGUESES!!!\n")
                        if fregueses_servidos % n_fregueses == 0:
                            rodada_atual += 1
                    
                    if fila1.tamanho() > 0:
                        fregues_executando = fila1.proximo_fregues()
                    else:
                        if fila2.tamanho() > 0:
                            fregues_executando = fila2.proximo_fregues()
                        else:
                            fregues_executando = Fregues()
                            nao_tem_mais_ngm_p_chegar = 0

                else:
                    if id_proximo_fregues == n_fregueses:
                        #TENHO QUE ATUALIZAR O SISTEMA DIZENDO Q N TEM MAIS NGM PARA CHEGAR, QUE ESSE CARA QUE TEM Q RODAR.
                        nao_tem_mais_ngm_p_chegar = 1
                        if nao_tem_mais_ngm_p_chegar:
                            tempo = tempo + tempo_ate_prox_chegada
                            #print("\nTEMPO DE EXECUÇÃO: ", tempo)
                    fregues_executando.tempo_restante -= tempo_ate_prox_chegada
                    tempo_ate_prox_chegada = 0

            
                
            if id_proximo_fregues % 10 == 0:
                variancia_ns.append(fila1.calcula_variancia_ns(1, id_proximo_fregues))
                utilizacao.append((fila1.ns_med + fila2.ns_med)/id_proximo_fregues)

        fila1.atualiza_esperancas(n_fregueses)
        fila2.atualiza_esperancas(n_fregueses)
        fila1.imprime_esperancas()
        fila2.imprime_esperancas()

Simulador().executar(3, 1, 6)
# Plot().desenha_grafico(utilizacao, 'Numero de Fregueses', 'Utilizacao do Servidor')
# Plot().desenha_grafico(variancia_ns, 'Numero de Fregueses', 'Variancia de Ns')
