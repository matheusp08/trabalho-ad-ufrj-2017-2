""" Modulo Utils
"""

import math
import numpy.random as nprand

class Utils:
    """ Classe que contem metodos utilitarios
    """

    # semente parao programa sempre gerar os mesmo numeros aleatorios
    nprand.seed(42)

    @staticmethod
    def gera_taxa_exp_seed(taxa):
        """ Funcao para retornar um numero aleatorio que segue uma taxa exponencial
            com base na taxa de entrada e na semente
            Args:
                taxa: valor da taxa
            Returns:
                numero aleatorio seguindo uma taxa exponencial 
        """
        return -1*math.log(1 - nprand.rand(1)[0]) / taxa

    @staticmethod
    def gera_taxa_exp(taxa):
        """ Funcao para retornar um numero aleatorio que segue uma taxa exponencial
            com base na taxa de entrada
            Args:
                taxa: valor da taxa
            Returns:
                numero aleatorio seguindo uma taxa exponencial 
        """
        return nprand.exponential(taxa)

    @staticmethod
    def get_distribuicao_t_student():
        """ Funcao para retornar o valor da t-student para o intervalo de confianca 95%
        """
        return 1.96
