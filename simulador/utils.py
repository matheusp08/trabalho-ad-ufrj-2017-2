""" Modulo Utils
"""

import random
import math

class Utils:
    """ Classe que contem metodos utilitarios
    """
    @staticmethod
    def get_taxa_servico():
        """ retorna a taxa de servico
        """
        return -1*math.log(1 - random.uniform(0, 1))

    @staticmethod
    def gera_taxa_exponencial():
        """ metodo para gerar um numero aleatorio de uma distribuicao exponencial
        """
        return -1*math.log(1 - random.uniform(0, 1))

    @staticmethod
    def get_distribuicao_t_student():
        """ metodo para retornar o valor da t-student para o intervalo de confianca 95%
        """
        return 1.96
