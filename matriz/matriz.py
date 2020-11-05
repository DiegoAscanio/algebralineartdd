import pdb
import copy
import numpy
from itertools import permutations
from functools import reduce
from matriz.exceptions import *

class MatrizBiDimensional:
    def __init__(self,matriz):
        '''
            Define uma matriz bi-dimensional de M linhas por N colunas se o 
            parametro matriz for consistente, ou seja, se cada linha tem a 
            mesma quantidade de colunas. A condição abaixo só é verdadeira 
            quando todas as linhas tem a mesma quantidade de colunas. Tomando
            como exemplo matriz = [[ 2, 2],
                                   [ 1 ]]
            O codigo abaixo cria um vetor que armazena a quantidade de 
            colunas de cada linha e compara esse vetor, a si proprio invertido.
            Nesse caso, o vetor de quantidade de colunas de matriz seria 
            representado por [ 2, 1 ] (2 colunas na primeira linha e 1 na 
            segunda) e seu inverso matriz [::-1] seria [ 1, 2 ], que é 
            diferente de [ 2, 1 ], portanto condição falsa que torna a matriz 
            inconsistente
        '''
        if not [ len(linha) for linha in matriz ] == [ len(linha) for linha in matriz ] [::-1]:
            raise MatrizInconsistenteException('A matriz especificada é inconsistente em suas colunas')
        self.matriz = matriz
    def __setitem__(self, index, value):
        if len(value) != self.colunas:
            raise MatrizInconsistenteException('A quantidade de colunas da linha ' + str(index + 1) + ' é inconsistente')
        self.matriz[index] = value
    def __getitem__(self, index):
        return self.matriz[index]
    def __len__(self):
        return len(self.matriz)
    def __repr__(self):
        return '[' + '\n '.join([str(self[i]) for i in range(len(self.matriz))]) + ']'
    def __eq__(self, other):
        return self.matriz == other.matriz
    def __add__(self, other):
        if self.ordem != other.ordem:
            raise MatrizInconsistenteException('As matrizes devem possuir a mesma ordem para serem somadas')
        return MatrizBiDimensional([[self.matriz[i][j] + other.matriz[i][j] for j in range(self.colunas)] for i in range(self.linhas)])
    def __mul_escalar(self, escalar):
        return MatrizBiDimensional([[self[i][j] * escalar for j in range(self.colunas)] for i in range(self.linhas)])
    def __mul_matrizes(self, other):
        if self.colunas != other.linhas:
            raise MatrizInconsistenteException('O numero de colunas da matriz multiplicanda deve ser igual ao numero de linhas da matriz multiplicadora')
        return MatrizBiDimensional([[sum([self[i][k] * other[k][j] for k in range(self.colunas)]) for j in range(other.colunas)] for i in range(self.linhas)])
    def __mul__(self, other):
        if type(other) not in [int, float, complex, MatrizBiDimensional]:
            raise TermoMultiplicacaoInvalidoException('O termo da multiplicação é inválido! Somente são aceitos termos dos tipos int, float, complex e MatrizBiDimensional')
        return self.__mul_escalar(other) if type(other) in [int, float, complex] else self.__mul_matrizes(other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __sub__(self, other):
        if self.ordem != other.ordem:
            raise MatrizInconsistenteException('As matrizes devem possuir a mesma ordem para serem subtraidas')
        return MatrizBiDimensional([[self.matriz[i][j] - other.matriz[i][j] for j in range(self.colunas)] for i in range(self.linhas)])
    '''
        métodos privados para calcular forma escada linha reduzida
    '''
    def __operacao_elementar_multiplicar_linha_por_escalar(self, indice_linha, escalar, enfileirar_operacoes_elementares = False):
        if enfileirar_operacoes_elementares:
            self.fila_operacoes_elementares.append((self.__operacao_elementar_multiplicar_linha_por_escalar.__name__, (indice_linha, escalar)))
        self[indice_linha] = [self[indice_linha][j] * escalar for j in range(self.colunas)]
    def __operacao_elementar_permutar_duas_linhas(self, indice_primeira_linha, indice_segunda_linha, enfileirar_operacoes_elementares = False):
        if enfileirar_operacoes_elementares:
            self.fila_operacoes_elementares.append((self.__operacao_elementar_permutar_duas_linhas.__name__,(indice_primeira_linha, indice_segunda_linha)))
        self[indice_primeira_linha],self[indice_segunda_linha] = self[indice_segunda_linha],self[indice_primeira_linha]
    def __operacao_elementar_combinacao_linear_subtrair_linhas(self, indice_linha_minuenda, indice_linha_subtraenda, escalar_multiplicado_linha_subtraenda, enfileirar_operacoes_elementares = False):
        if enfileirar_operacoes_elementares:
            self.fila_operacoes_elementares.append((self.__operacao_elementar_combinacao_linear_subtrair_linhas.__name__,(indice_linha_minuenda, indice_linha_subtraenda, escalar_multiplicado_linha_subtraenda)))
        self[indice_linha_minuenda] = [ (self[indice_linha_minuenda][j] - escalar_multiplicado_linha_subtraenda * self[indice_linha_subtraenda][j]) for j in range(self.colunas) ]
    def __organizar_linhas_nulas_e_nao_nulas(self):
        self.matriz = list(filter(lambda x: x.count(0) != self.colunas, self)) + list(filter(lambda x: x.count(0) == self.colunas, self))
    def __linhas_elementos_nao_nulos_da_coluna_j(self, j):
        return list(map(lambda x: x[1], list(filter(lambda x: x[0] != 0, zip(self.coluna(j),range(self.linhas))))))
    def __linhas_candidatas_para_permutacao_coluna_j(self, i, j):
        return list(filter(lambda x: x > i, self.__linhas_elementos_nao_nulos_da_coluna_j(j)))
    def __tentar_transformar_elemento_ij_em_nao_nulo(self, i, j, enfileirar_operacoes_elementares = False):
        self.__operacao_elementar_permutar_duas_linhas(i, self.__linhas_candidatas_para_permutacao_coluna_j(i, j)[0], enfileirar_operacoes_elementares) if len(self.__linhas_candidatas_para_permutacao_coluna_j(i, j)) > 0 else None
    def __transformar_elemento_ij_nao_nulo_em_1(self, i, j, enfileirar_operacoes_elementares = False):
        self.__operacao_elementar_multiplicar_linha_por_escalar(i, self[i][j]**(-1), enfileirar_operacoes_elementares) if self[i][j] != 0 else None
    def __transformar_demais_elementos_kj_em_nulos(self, i, j, enfileirar_operacoes_elementares = False):
        for k in list(range(0, i)) + list(range(i + 1, self.linhas)):
            self.__operacao_elementar_combinacao_linear_subtrair_linhas(k, i, self[k][j], enfileirar_operacoes_elementares) if self[k][j] != 0 else None
    '''
        métodos privados utilizados para calculo de determinante atraves de produtorio de permutacoes
    '''
    def __determinante_somatorio_produtorio_das_permutacoes(self):
        return float(sum([ self.__sinal_permutacao(permutacao) * self.__produtorio(permutacao) for permutacao in self.__lista_permutacoes()]))
    def __lista_permutacoes(self):
        return list(permutations(range(self.linhas)))
    def __composicao_pares_ordenados(self, i):
        return [ (i, j) for j in range(i + 1, self.linhas) ]
    def __pares_ordenados_para_verificacao_de_sinal_de_permutacoes(self):
        pares = []
        for i in range(self.linhas - 1):
            pares += self.__composicao_pares_ordenados(i)
        return pares
    def __sinal_permutacao(self, permutacao):
        return 1 if sum([ 1 if permutacao[i] > permutacao[j] else 0 for i, j in self.__pares_ordenados_para_verificacao_de_sinal_de_permutacoes()]) % 2 == 0 else -1
    def __produtorio(self, permutacao):
        return reduce (lambda x, y: x*y, [ self[i][j] for i, j in zip(range(self.linhas), permutacao)])
    '''
        métodos privados utilizados para calculo de determinante atraves de cofatores
    '''
    def __determinante_cofatores(self):
        return self[0][0] if self.ordem == (1,1) else sum([self[0][j] * self.__cofator(0, j) for j in range(self.colunas)])
    def __cofator(self, i,j):
        return (-1) ** (i + j) * MatrizBiDimensional([[self[k][l] for k in list(range(0,i)) + list(range(i + 1, self.linhas))] for l in list(range(0,j)) + list(range(j+1, self.colunas))]).determinante()
    '''
        métodos privados para cálculo de matriz inversa através da fila de operacoes elementares
    '''
    def __inversa_por_fila_de_operacoes_elementares(self):
        self.forma_escada_linha_reduzida(enfileirar_operacoes_elementares = True)
        inversa = MatrizBiDimensional.identidade(self.linhas)
        for nome_operacao_elementar, argumentos in self.fila_operacoes_elementares:
            for operacao_elementar in [inversa._MatrizBiDimensional__operacao_elementar_multiplicar_linha_por_escalar, inversa._MatrizBiDimensional__operacao_elementar_permutar_duas_linhas, inversa._MatrizBiDimensional__operacao_elementar_combinacao_linear_subtrair_linhas]:
                if operacao_elementar.__name__ == nome_operacao_elementar:
                    operacao_elementar(*argumentos)
        del(self.fila_operacoes_elementares)
        return inversa
    '''
        métodos privados para cálculo de matriz inversa através da adjunta clássica
    '''  
    def __inversa_por_adjunta_classica(self):
        return (1/self.determinante()) * self.adjunta()

    @property
    def linhas(self):
        return len(self)
    @property
    def colunas(self):
        return 0 if len(self) == 0 else len(self[0])
    @property
    def ordem(self):
        return (self.linhas, self.colunas)
    @property
    def nulidade(self):
        return self.colunas - self.posto
    @property
    def posto(self):
        return len(list(filter(lambda x: x.count(0) != self.colunas, self)))
    @staticmethod
    def zeros(M, N=None):
        return MatrizBiDimensional([[0 for i in range(N)] for j in range(M)] if N != None else [[0 for i in range(M)] for j in range(M)])
    @staticmethod
    def identidade(M):
        return MatrizBiDimensional([[1 if j == i else 0 for j in range(M)] for i in range(M)])

    def linha(self, index):
        return self[index]
    def coluna(self, index):
        return [self[i][index] for i in range(len(self))]
    def transpor(self):
        return MatrizBiDimensional([[self[j][i] for j in range(self.linhas)] for i in range(self.colunas)])
    def conjugar(self):
        return MatrizBiDimensional([[self[i][j].conjugate() for j in range(self.colunas)] for i in range(self.linhas)])
    def transposto_hermitiano(self):
        return self.transpor().conjugar()
    def forma_escada_linha_reduzida(self, enfileirar_operacoes_elementares = False):
        self.fila_operacoes_elementares = []
        other = copy.deepcopy(self)
        other.__organizar_linhas_nulas_e_nao_nulas()
        i = 0
        j = 0
        quantidade_pivos = 0
        while j < self.colunas and quantidade_pivos < self.posto:
            '''
                gambiarra para forma escada linha reduzida funcionar com numeros irracionais
                depois implementar funcao propria isclose
            '''
            if numpy.isclose(other[i][j], 0):
            #if other[i][j] == 0:
                other.__tentar_transformar_elemento_ij_em_nao_nulo(i, j, enfileirar_operacoes_elementares)
            if not numpy.isclose(other[i][j], 0):
            #if other[i][j] != 0:
                other.__transformar_elemento_ij_nao_nulo_em_1(i, j, enfileirar_operacoes_elementares)
                other.__transformar_demais_elementos_kj_em_nulos(i, j, enfileirar_operacoes_elementares)
                quantidade_pivos += 1
                i = i + 1 if i < self.linhas - 1 else i
            j = j + 1
        if enfileirar_operacoes_elementares:
            self.fila_operacoes_elementares = other.fila_operacoes_elementares
        return other
    def determinante(self, metodo_cofatores = True):
        if self.linhas != self.colunas:
            raise MatrizInconsistenteException('A ordem da matriz deve ser quadrada para que seu determinante possa ser calculado')
        return self.__determinante_cofatores() if metodo_cofatores else self.__determinante_somatorio_produtorio_das_permutacoes()
    def cofator(self, i, j):
        return self.__cofator(i, j)
    def cofatores(self):
        if self.linhas != self.colunas:
            raise MatrizInconsistenteException('A matriz especificada não é quadrada, portanto, não pode ter matriz de cofatores calculada!')
        return MatrizBiDimensional([[self.__cofator(i, j) for j in range(self.colunas)] for i in range(self.linhas)])
    def adjunta(self):
        return self.cofatores().transpor()
    def inversa(self, metodo_adjunta_classica = True):
        if self.determinante() == 0:
            raise MatrizSingularException('A matriz especificada é singular e não pode ser invertida!')
        return self.__inversa_por_adjunta_classica() if metodo_adjunta_classica else self.__inversa_por_fila_de_operacoes_elementares()
