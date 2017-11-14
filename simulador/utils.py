""" Modulo Utils
"""

import math
import numpy.random as nprand

class Utils:
    """ Classe que contem metodos utilitarios
    """

    nprand.seed(42)

    @staticmethod
    def gera_taxa_exp_seed(taxa):
        """ retorna a taxa exponencial dado uma semente
        """
        return -1*math.log(1 - nprand.rand(1)[0]) / taxa

    @staticmethod
    def gera_taxa_exp(taxa):
        """ retorna a taxa exponencial
        """
        return nprand.exponential(taxa)

    @staticmethod
    def get_distribuicao_t_student():
        """ metodo para retornar o valor da t-student para o intervalo de confianca 95%
        """
        return 1.96
