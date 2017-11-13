"""Classe principal do Simulador"""

import fila as f

class Simulador:
    """Classe do simulador
    Args:
        taxa_entrada: taxa de entrada do sistema
        n_rodadas: numero de rodadas da simulacao
        rho: taxa de servico
    Returns:
        nada
    """
    def executar(self, taxa_entrada, n_rodadas, rho):
        """Funcao de execucao do simulador
        Args:
            taxa_entrada: taxa de entrada do sistema
            n_rodadas: numero de rodadas da simulacao
            rho: taxa de servico
        Returns:
            nada
        """
        print("Numero de rodadas: %d" % n_rodadas)
        print("Taxa de servico rho: %f" % rho)
        f.Fila("FCFS", 1, taxa_entrada)
        f.Fila("FCFS", 2, taxa_entrada)


# INICIO DO PROGRAMA
Simulador().executar(1.2, 100, 0.2)
