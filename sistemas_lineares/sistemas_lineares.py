import pdb
import copy

from matriz.matriz import MatrizBiDimensional
from sistemas_lineares.exceptions import SLInvalidoException, SLInsolucionavelException

class SL:
    def __coeficientes_e_termos_independentes_validos(self, A, B):
        return False if type(A) != MatrizBiDimensional or type(B) != MatrizBiDimensional or A.linhas != B.linhas or B.colunas != 1 else True
    def __init__(self, A, B):
        if not self.__coeficientes_e_termos_independentes_validos(A, B):
            raise SLInvalidoException('Coeficientes e/ou Termos Independentes Inválidos! Os coeficientes e termos independente devem ser do tipo MatrizBiDimensional; O numero de linhas da matriz de coeficientes deve ser igual ao número de linhas da matriz de termos independentes; A matriz de termos independentes deve ser uma matriz coluna')
        self.A, self.B = A, B
    def __eq__(self, other):
        return self.A, self.B == other.A, other.B

    def __matriz_aumentada(self):
        return MatrizBiDimensional([[self.A[i][j] for j in range(self.A.colunas)] + self.B[i] for i in range(self.equacoes)])
    def __matriz_coeficientes_quadrada(self):
        return self.A.linhas == self.A.colunas
    def __aplicar_forma_linha_reduzida_para_construir_matriz_solucao(self):
        self.__matriz_solucao = self.__matriz_aumentada().forma_escada_linha_reduzida()
    def __separar_coeficientes_termos_independentes_matriz_solucao(self):
        self.__coeficientes_matriz_solucao = MatrizBiDimensional([[self.__matriz_solucao[i][j] for j in range(self.A.colunas)] for i in range(self.A.linhas)])
        self.__termos_independentes_matriz_solucao = MatrizBiDimensional([[self.__matriz_solucao[i][-1]] for i in range(self.B.linhas)])
    def __str_solucao(self):
        str_solucao = ''
        for variavel, termos_composicao in zip(self.solucao.keys(), self.solucao.values()):
            termo_independente, outras_variaveis = termos_composicao[0], termos_composicao[1]
            str_solucao += 'X_' + str(variavel) + ' = ' + str(termo_independente)
            for outra_variavel in outras_variaveis:
                str_solucao += ' + {1}X_{0}'.format(outra_variavel[0], outra_variavel[1]) if outra_variavel[1] > 0 else ' {1}X_{0}'.format(outra_variavel[0], outra_variavel[1]) if outra_variavel[1] < 0 else ''
            str_solucao += '\n'
        return str_solucao
    def __solucao_forma_escada_linha_reduzida(self):
        self.__aplicar_forma_linha_reduzida_para_construir_matriz_solucao()
        self.__separar_coeficientes_termos_independentes_matriz_solucao()
        self.solucao = {}
        for i in range(self.__coeficientes_matriz_solucao.linhas):
            for j in range(i, self.__coeficientes_matriz_solucao.colunas):
                if self.__coeficientes_matriz_solucao[i][j] == 1:
                    self.solucao[j] = ((self.__termos_independentes_matriz_solucao[i][0], [ (k, -1 * self.__coeficientes_matriz_solucao[i][k]) for k in list(range(0,j)) + list(range(j + 1, self.__coeficientes_matriz_solucao.colunas))]))
                    break
        print(self.__str_solucao())
        return self.solucao
    def __solucao_regra_crammer(self):
        self.solucao = {}
        for j in range(self.A.colunas):
            crammer = copy.deepcopy(self.A)
            for i in range(self.A.linhas):
                crammer[i][j] = self.B[i][0]
            self.solucao[j] = (crammer.determinante() / self.A.determinante(), [])
        print(self.__str_solucao())
        return self.solucao
    @property
    def incognitas(self):
        return self.A.colunas
    @property
    def equacoes(self):
        return self.A.linhas
    @property
    def solucionavel(self):
        return self.__matriz_aumentada().forma_escada_linha_reduzida().posto == self.A.forma_escada_linha_reduzida().posto

    def resolver(self):
        if not self.solucionavel:
            raise SLInsolucionavelException('O sistema especificado não possui solução')
        return self.__solucao_forma_escada_linha_reduzida() if not self.__matriz_coeficientes_quadrada() or self.A.determinante() == 0 else self.__solucao_regra_crammer()
