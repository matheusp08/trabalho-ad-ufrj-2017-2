""" Modulo Fregues
"""

import utils as u

class Fregues:
    """ Classe que representa os fregueses do sistema
    """

    def __init__(self):
        self.taxa_servico = u.Utils.gera_taxa_exp(0.2)

    def imprime_parametros(self):
        """Funcao para imprimir os parametros do fregues
            Args:
                Nenhum argumento
            Returns:
                Nenhum retorno
        """
        print("Taxa de servico: %f" % self.taxa_servico)
