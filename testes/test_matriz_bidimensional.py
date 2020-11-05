import pytest
import random
import copy
from itertools import permutations

from matriz.matriz import MatrizBiDimensional
from matriz.exceptions import *
from testes.utils import wolfram_escalonamento_linha_reduzido, wolfram_determinante

wolfram_disabled = True

def test_excecao_matriz_inconsistente():
    with pytest.raises(MatrizInconsistenteException) as excinfo:
        matriz = MatrizBiDimensional([[1,2],[1]])
    assert "A matriz especificada é inconsistente em suas colunas" in str(excinfo.value)   

def test_repr_matriz_3x3_1_a_9():
    matriz = MatrizBiDimensional([[1, 2, 3],\
                                  [4, 5, 6],\
                                  [7, 8, 9]])
    assert repr(matriz) == '[[1, 2, 3]\n'+\
                           ' [4, 5, 6]\n'+\
                           ' [7, 8, 9]]'

def test_repr_matriz_3x3_9_a_1():
    matriz = MatrizBiDimensional([[9, 8, 7],
                                  [6, 5, 4],
                                  [3, 2, 1]])
    assert repr(matriz) == '[[9, 8, 7]\n'+\
                           ' [6, 5, 4]\n'+\
                           ' [3, 2, 1]]'

def test_matriz_linha_1():
    matriz = MatrizBiDimensional([[1, 2, 3],\
                                  [4, 5, 6],\
                                  [7, 8, 9]])
    assert matriz.linha(0) == [1, 2, 3]

def test_matriz_coluna_3():
    matriz = MatrizBiDimensional([[1, 2, 3],\
                                  [4, 5, 6],\
                                  [7, 8, 9]])
    assert matriz.coluna(2) == [3, 6, 9]

def test_getitem_linha_2():
    matriz = MatrizBiDimensional([[1, 2, 3],\
                                  [4, 5, 6],\
                                  [7, 8, 9]])
    assert matriz[1] == [4, 5, 6]

def test_getitem_linha_2_coluna_3():
    matriz = MatrizBiDimensional([[1, 2, 3],\
                                  [4, 5, 6],\
                                  [7, 8, 9]])
    assert matriz[1][2] == 6

def test_property_linhas():
    matriz = MatrizBiDimensional([[1, 2, 3],\
                                  [4, 5, 6],\
                                  [7, 8, 9]])
    assert matriz.linhas == 3

def test_property_colunas():
    matriz = MatrizBiDimensional([[1, 2, 3],\
                                  [4, 5, 6],\
                                  [7, 8, 9]])
    assert matriz.colunas == 3

def test_property_ordem():
    matriz = MatrizBiDimensional([[1, 2, 3],\
                                  [4, 5, 6]])
    assert matriz.ordem == (2, 3)

def test_soma_a_b():
    a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    b = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    assert a + b == MatrizBiDimensional([[2, 4, 6],\
                                         [8, 10, 12]])

def test_a_mais_igual_b():
    a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    b = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    a += b
    assert a == MatrizBiDimensional([[2, 4, 6],\
                                     [8, 10, 12]])

def test_excecao_soma_matrizes_ordens_distintas():
    with pytest.raises(MatrizInconsistenteException) as excinfo:
        a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
        b = MatrizBiDimensional([[1, 2, 3]])
        a + b
    assert "As matrizes devem possuir a mesma ordem para serem somadas" in str(excinfo.value) 

def test_subtracao_a_b():
    a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    b = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    assert a - b == MatrizBiDimensional([[0, 0, 0],\
                                         [0, 0, 0]])

def test_a_menos_igual_b():
    a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    b = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    a -= b
    assert a == MatrizBiDimensional([[0, 0, 0],\
                                     [0, 0, 0]])

def test_excecao_subtrair_matrizes_ordens_distintas():
    with pytest.raises(MatrizInconsistenteException) as excinfo:
        a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
        b = MatrizBiDimensional([[1, 2, 3]])
        a - b
    assert "As matrizes devem possuir a mesma ordem para serem subtraidas" in str(excinfo.value) 


def test_atualizar_linha_2():
    a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    a[1] = [6, 5, 4]
    assert a == MatrizBiDimensional([[1, 2, 3],\
                                     [6, 5, 4]])

def test_excecao_atualizar_linha_2():
    with pytest.raises(MatrizInconsistenteException) as excinfo:
        a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
        a[1] = [5, 6]
    assert "A quantidade de colunas da linha 2 é inconsistente" in str(excinfo.value)

def test_multiplicar_matriz_a_por_2():
    a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    assert 2 * a == MatrizBiDimensional([[2, 4, 6],\
                                         [8, 10, 12]])

def test_propriedade_distributiva_multiplicacao_escalar():
    a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    b = MatrizBiDimensional([[1, 1, 1],\
                             [1, 1, 1]])
    l = 3
    assert l * (a + b) == l*a + l*b

def test_propriedade_distributiva_relacionada_a_numeros_multiplicacao_escalar():
    A = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    a = 3
    b = 4
    assert (a + b) * A == a*A + b*A

def test_propriedade_multiplicacao_escalar_por_zero():
    A = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    assert 0*A == MatrizBiDimensional([[0, 0, 0],\
                                       [0, 0, 0]])

def test_metodo_estatico_zeros_matriz_quadrada_ordem_3():
    A = MatrizBiDimensional.zeros(3)
    assert A == MatrizBiDimensional([[0 for j in range(3)] for i in range(3)])

def test_metodo_estatico_zeros_matriz_quadrada_ordem_1000():
    A = MatrizBiDimensional.zeros(1000)
    assert A == MatrizBiDimensional([[0 for j in range(1000)] for i in range(1000)])

def test_metodo_estatico_zeros_matriz_ordem_2_3():
    A = MatrizBiDimensional.zeros(2,3)
    assert A == MatrizBiDimensional([[0 for j in range(3)] for i in range(2)])

def test_metodo_estatico_zeros_matriz_ordem_2000_3000():
    A = MatrizBiDimensional.zeros(2000,3000)
    assert A == MatrizBiDimensional([[0 for j in range(3000)] for i in range(2000)])

def test_multiplica_matriz_1_2_por_matriz_2_1():
    A = MatrizBiDimensional([[1, 2]])
    B = MatrizBiDimensional([[2],\
                             [1]])
    assert A * B == MatrizBiDimensional([[4]])

def test_multiplica_matriz_4_3_por_matriz_3_1():
    A = MatrizBiDimensional([[1, 1, 1],\
                             [2, 2, 2],\
                             [3, 3, 3],\
                             [4, 4, 4]])
    B = MatrizBiDimensional([[1],\
                             [2],\
                             [3]])
    assert A * B == MatrizBiDimensional([[6],\
                                         [12],\
                                         [18],\
                                         [24]])

def test_multiplica_matriz_4_1_por_matriz_1_4():
    A = MatrizBiDimensional([[1],\
                             [1],\
                             [1],\
                             [1]])
    B = MatrizBiDimensional([[4, 4, 4, 4]])
    assert A * B == MatrizBiDimensional([[4, 4, 4, 4],\
                                         [4, 4, 4, 4],\
                                         [4, 4, 4, 4],\
                                         [4, 4, 4, 4]])
def test_excecao_multiplicar_matrizes_dimensoes_inconsistentes():
    with pytest.raises(MatrizInconsistenteException) as excinfo:
        A = MatrizBiDimensional([[1],\
                                 [1],\
                                 [1],\
                                 [1]])
        B = MatrizBiDimensional([[4],\
                                 [4],\
                                 [4],\
                                 [4]])
        A * B
    assert "O numero de colunas da matriz multiplicanda deve ser igual ao numero de linhas da matriz multiplicadora" in str(excinfo.value)

def test_excecao_multiplicar_tipo_nao_implementado():
    with pytest.raises(TermoMultiplicacaoInvalidoException) as excinfo:
        A = MatrizBiDimensional([[1],\
                                 [1],\
                                 [1],\
                                 [1]])
        A * 'a'
    assert "O termo da multiplicação é inválido! Somente são aceitos termos dos tipos int, float, complex e MatrizBiDimensional" in str(excinfo.value)

def test_i_propriedade_multiplicacao_matrizes_ab_em_geral_diferente_ba():
    A = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6],\
                             [7, 8, 9]])
    B = MatrizBiDimensional([[7, 8, 9],\
                             [4, 5, 6],\
                             [1, 2, 3]])
    assert A*B != B*A

def test_ii_propriedade_multiplicacao_matrizes_distributividade():
    A = MatrizBiDimensional([[1, 2, 3]])
    B = MatrizBiDimensional([[4],\
                             [5],\
                             [6]])
    C = MatrizBiDimensional([[7],\
                             [8],\
                             [9]])
    assert A*(B + C) == A*B + A*C

def test_iii_propriedade_multiplicacao_matrizes_aleatorias_1xm_mx1_m_aleatorio_distributividade():
    m = random.randint(1,100)
    A = MatrizBiDimensional([[random.randint(1,1000) for i in range(m)]])
    D = MatrizBiDimensional([[random.randint(1,1000) for i in range(m)]])
    B = MatrizBiDimensional([[random.randint(1,1000)] for i in range(m)])
    assert (A + D) * B == A*B + D*B

def test_iv_propriedade_associatividade_matrizes_quadradas_aleatorias_ordem_mxn_nxo_oxp_m_n_o_p_aleatorios():
    m = random.randint(1,100)
    n = random.randint(1,100)
    o = random.randint(1,100)
    p = random.randint(1,100)
    A = MatrizBiDimensional([[random.randint(1,1000) for j in range(n)] for i in range(m)])
    B = MatrizBiDimensional([[random.randint(1,1000) for j in range(o)] for i in range(n)])
    E = MatrizBiDimensional([[random.randint(1,1000) for i in range(p)] for i in range(o)])
    assert (A*B)*E == A*(B*E)

def test_v_propriedade_multiplicacao_elemento_neutro_matriz_quadrada_A_aleatoria_ordem_m_aleatoria_matriz_identidade_ordem_m_aleatoria():
    m = random.randint(1,100)
    A = MatrizBiDimensional([[random.randint(1,1000) for j in range(m)] for i in range(m)])
    I = MatrizBiDimensional.identidade(m)
    assert A*I == I*A == A

def test_transpor_matriz_A_2x3():
    A = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
    assert A.transpor() == MatrizBiDimensional([[1, 4],\
                                                [2, 5],\
                                                [3, 6]])

def test_transpor_matriz_A_aleatoria_ordem_mxn_aleatorios():
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[random.randint(1,1000) for j in range(n)] for i in range(m)])
    A_transposta = MatrizBiDimensional([[A[j][i] for j in range(m)] for i in range(n)])
    assert A.transpor() == A_transposta

def test_i_propriedade_transposicao_A_aleatoria_transposta_transposta_igual_A():
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[random.randint(1,1000) for j in range(n)] for i in range(m)])
    assert A.transpor().transpor() == A

def test_ii_propriedade_transposicao_soma_A_B_transposta_igual_soma_A_transposta_B_transposta():
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[random.randint(1,1000) for j in range(n)] for i in range(m)])
    B = MatrizBiDimensional([[random.randint(1,1000) for j in range(n)] for i in range(m)])
    assert (A + B).transpor() == A.transpor() + B.transpor()

def test_iii_propriedade_transposicao_escalar_multiplicado_A_transpostos_igual_escalar_multiplicado_A_transposta():
    l = random.randint(1,100)
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[random.randint(1,1000) for j in range(n)] for i in range(m)])
    assert (l*A).transpor() == l*A.transpor()

def test_iv_propriedade_transposicao_A_B_multiplicados_transposta_igual_B_transposta_multiplicado_A_transposta():
    m = random.randint(1,100)
    n = random.randint(1,100)
    o = random.randint(1,100)
    A = MatrizBiDimensional([[random.randint(1,1000) for j in range(n)] for i in range(m)])
    B = MatrizBiDimensional([[random.randint(1,1000) for j in range(o)] for i in range(n)])
    assert (A*B).transpor() == B.transpor() * A.transpor()

def test_v_propriedade_transposicao_se_A_simetrica_A_transposta_igual_A():
    m = random.randint(1,100)
    A = MatrizBiDimensional.zeros(m)
    for i in range(m):
        for j in range(i, m):
            A[i][j] = A[j][i] = random.randint(-100,100)
    assert A.transpor() == A

def test_conjugar_matriz_A_2x2_numeros_complexos():
    A = MatrizBiDimensional([[complex(1,2), complex(-3,-5)],\
                             [13,           complex(0,-8)]])
    A_conjugada = MatrizBiDimensional([[A[i][j].conjugate() for j in range(2)] for i in range(2)])
    assert A.conjugar() == A_conjugada

def test_conjugar_matriz_A_complexa_aleatoria_mxn_aleatorios():
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[complex(random.randint(-10,10),random.randint(-10,10)) for j in range(n)] for i in range(m)])
    A_conjugada = MatrizBiDimensional([[A[i][j] if type(A[i][j]) != complex else A[i][j].conjugate() for j in range(n)] for i in range(m)])
    assert A.conjugar() == A_conjugada

def test_dagger_conhecido_como_transposto_hermitiano():
    A = MatrizBiDimensional([[1,                         0],\
                             [complex(0,-2), complex(4, 1)],\
                             [complex(0, 9),             5]])
    A_dagger = A.transpor().conjugar()
    assert A.transposto_hermitiano() == A_dagger

def test_dagger_conhecido_como_transposto_hermitiano_matriz_A_complexa_aleatoria_mxn_aleatorios():
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[complex(random.randint(-10,10),random.randint(-10,10)) for j in range(n)] for i in range(m)])

    A_dagger = A.transpor().conjugar()
    assert A.transposto_hermitiano() == A_dagger

def test_i_propriedade_conjugacao_hermitiana_matriz_A_complexa_aleatoria_mxn_aleatorios():
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[complex(random.randint(-10,10),random.randint(-10,10)) for j in range(n)] for i in range(m)])
    assert A.transposto_hermitiano().transposto_hermitiano() == A

def test_ii_propriedade_conjugacao_hermitiana_matrizes_A_B_complexas_aleatorias_mxn_aleatorios():
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[complex(random.randint(-10,10),random.randint(-10,10)) for j in range(n)] for i in range(m)])
    B = MatrizBiDimensional([[complex(random.randint(-10,10),random.randint(-10,10)) for j in range(n)] for i in range(m)])
    assert (A + B).transposto_hermitiano() == A.transposto_hermitiano() + B.transposto_hermitiano()

def test_iii_propriedade_conjugacao_hermitiana_matriz_A_complexa_aleatoria_mxn_aleatorios_escalar_complexo_aleatorio():
    m = random.randint(1,100)
    n = random.randint(1,100)
    A = MatrizBiDimensional([[complex(random.randint(-10,10),random.randint(-10,10)) for j in range(n)] for i in range(m)])
    escalar_complexo = complex(random.uniform(-100,100), random.randint(-1,1))
    assert (escalar_complexo * A).transposto_hermitiano() == escalar_complexo.conjugate() * A.transposto_hermitiano()

def test_iv_propriedade_conjugacao_hermitiana_matrizes_A_B_complexas_aleatorias_mxn_aleatorios():
    m = random.randint(1,100)
    n = random.randint(1,100)
    o = random.randint(1,100)
    A = MatrizBiDimensional([[complex(random.randint(-10,10),random.randint(-10,10)) for j in range(n)] for i in range(m)])
    B = MatrizBiDimensional([[complex(random.randint(-10,10),random.randint(-10,10)) for j in range(o)] for i in range(n)])
    assert (A * B).transposto_hermitiano() == B.transposto_hermitiano() * A.transposto_hermitiano()

def test_v_propriedade_se_A_matriz_hermitiana_A_transposto_hermitiano_igual_A():
    m = random.randint(1,100)
    A = MatrizBiDimensional.zeros(m)
    complexo_e_conjugado = lambda x: (x, x.conjugate())
    for i in range(m):
        for j in range(i, m):
            A[i][j],A[j][i] = complexo_e_conjugado(random.uniform(-100,100)) if i == j else complexo_e_conjugado(complex(random.uniform(-100,100),random.uniform(-100,100)))
    assert A.transposto_hermitiano() == A

def test_private_operacao_elementar_multiplicar_linha_2_matriz_identidade_por_3():
    A = MatrizBiDimensional.identidade(3)
    A._MatrizBiDimensional__operacao_elementar_multiplicar_linha_por_escalar(1,3)
    assert A == MatrizBiDimensional([[1, 0, 0],\
                                     [0, 3, 0],\
                                     [0, 0, 1]])

def test_private_operacao_elementar_permutar_linha_1_linha_2_matriz_identidade():
    A = MatrizBiDimensional.identidade(3)
    A._MatrizBiDimensional__operacao_elementar_permutar_duas_linhas(0,1)
    assert A == MatrizBiDimensional([[0, 1, 0],\
                                     [1, 0, 0],\
                                     [0, 0, 1]])

def test_private_operacao_elementar_combinacao_linear_linha_1_igual_linha_1_mais_8_vezes_linha_2():
    A = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6],\
                             [7, 8, 9]])
    A._MatrizBiDimensional__operacao_elementar_combinacao_linear_subtrair_linhas(0, 1, -8)
    assert A == MatrizBiDimensional([[33, 42, 51],\
                                     [ 4,  5,  6],\
                                     [ 7,  8,  9]])

def test_posto_nulidade_matriz_A_6x8_2_linhas_nulas():
    A = MatrizBiDimensional([[random.randint(-10,10) for j in range(8)] for i in range(3) ] + [ [0 for j in range(8)] ] + [ [random.randint(-10,10) for j in range(8)] ] + [ [0 for j in range(8)] ])
    assert (4, 4) == (A.posto, A.nulidade)


def test_private_organizar_linhas_nulas_e_nao_nulas():
    A = MatrizBiDimensional([[random.randint(-10,10) for j in range(8)] for i in range(3) ] + [ [0 for j in range(8)] ] + [ [random.randint(-10,10) for j in range(8)] ] + [ [0 for j in range(8)] ])
    B = copy.copy(A)
    A._MatrizBiDimensional__organizar_linhas_nulas_e_nao_nulas()
    assert A == MatrizBiDimensional(B[0:3] + [B[4]] + [B[3]] + [B[5]])

def test_private_tentar_transformar_elemento_ij_em_nao_nulo():
    A = MatrizBiDimensional([[0, 1, 1], [1, 1, 1], [2, 2, 2]])
    A._MatrizBiDimensional__tentar_transformar_elemento_ij_em_nao_nulo(0, 0)
    assert A == MatrizBiDimensional([[1, 1, 1], [0, 1, 1], [2, 2, 2]])

def test_private_transformar_demais_elementos_kj_em_nulos():
    A = MatrizBiDimensional([[1,  1,  1,  6],\
                             [4, -3,  2,  0],\
                             [2, -1,  3, 11],\
                             [3,  1,  1,  4]])
    A._MatrizBiDimensional__transformar_demais_elementos_kj_em_nulos(0, 0)
    assert A == MatrizBiDimensional([[1,  1,  1,   6],\
                                     [0, -7, -2, -24],\
                                     [0, -3,  1,  -1],\
                                     [0, -2, -2, -14]])

@pytest.mark.skipif(wolfram_disabled, reason="Feature com recursos limitados!")
def forma_escada_linha_reduzida_matriz_aleatoria_com_verificacao_no_wolfram_alpha():
    linhas  = random.randint(4, 6)
    colunas = random.randint(3, 8)
    A = MatrizBiDimensional([[random.randint(-10,10) for j in range(colunas)] for i in range(linhas)])
    A_felr = A.forma_escada_linha_reduzida()
    A_welr = wolfram_escalonamento_linha_reduzido(A)
    A_felr = MatrizBiDimensional([[round(A_felr[i][j], 4) for j in range(A_felr.colunas)] for i in range(A_felr.linhas)])
    A_welr = MatrizBiDimensional([[round(A_welr[i][j], 4) for j in range(A_welr.colunas)] for i in range(A_welr.linhas)])
    return A_felr == A_welr

@pytest.mark.skipif(wolfram_disabled, reason="Feature com recursos limitados!")
def test_forma_escada_linha_reduzida_matrizes_aleatorias_1_vez():
    for i in range(1):
        assert True == forma_escada_linha_reduzida_matriz_aleatoria_com_verificacao_no_wolfram_alpha()


@pytest.mark.skipif(wolfram_disabled, reason="Feature com recursos limitados!")
def test_forma_escada_linha_reduzida_matriz_psicodelica():
    A = MatrizBiDimensional([[1 for j in range(5)], [2 for j in range(5)], [3 for j in range(5)]] + [[0 for j in range(5)] for i in range(2)])
    A_felr = A.forma_escada_linha_reduzida()
    A_welr = wolfram_escalonamento_linha_reduzido(A)
    A_felr = MatrizBiDimensional([[round(A_felr[i][j], 4) for j in range(A_felr.colunas)] for i in range(A_felr.linhas)])
    A_welr = MatrizBiDimensional([[round(A_welr[i][j], 4) for j in range(A_welr.colunas)] for i in range(A_welr.linhas)])
    assert A_felr == A_welr

def test_private_lista_permutacoes_matriz_quadrada_ordem_m_aleatorio():
    m = random.randint(1,6)
    A = MatrizBiDimensional.identidade(m)
    assert A._MatrizBiDimensional__lista_permutacoes() == list(permutations(range(m)))

def test_private_pares_ordenados_para_verificacao_de_sinal_de_permutacoes_matriz_ordem_3():
    A = MatrizBiDimensional.identidade(3)
    assert A._MatrizBiDimensional__pares_ordenados_para_verificacao_de_sinal_de_permutacoes() == [(0,1),(0,2),(1,2)]

def test_private_pares_ordenados_para_verificacao_de_sinal_de_permutacoes_matriz_ordem_5():
    A = MatrizBiDimensional.identidade(5)
    assert A._MatrizBiDimensional__pares_ordenados_para_verificacao_de_sinal_de_permutacoes() == [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]

def test_private_sinal_permutacao_0_2_1():
    A = MatrizBiDimensional.identidade(3)
    assert A._MatrizBiDimensional__sinal_permutacao([0, 2, 1]) == -1

def test_private_sinal_permutacao_1_0_2():
    A = MatrizBiDimensional.identidade(3)
    assert A._MatrizBiDimensional__sinal_permutacao([1, 2, 0]) == 1

def test_private_produtorio_permutacao_0_2_1():
    A = MatrizBiDimensional([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert A._MatrizBiDimensional__produtorio([0, 2, 1]) == 1*6*8

def test_private_produtorio_permutacao_2_1_0():
    A = MatrizBiDimensional([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert A._MatrizBiDimensional__produtorio([2, 1, 0]) == 3*5*7

def test_private_determinante_somatorio_produtorio_das_permutacoes():
    A = MatrizBiDimensional([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert A._MatrizBiDimensional__determinante_somatorio_produtorio_das_permutacoes() == 0

def test_excecao_determinante_matriz_nao_quadrada():
    with pytest.raises(MatrizInconsistenteException) as excinfo:
        a = MatrizBiDimensional([[1, 2, 3],\
                             [4, 5, 6]])
        a.determinante()
    assert "A ordem da matriz deve ser quadrada para que seu determinante possa ser calculado" in str(excinfo.value) 


@pytest.mark.skipif(wolfram_disabled, reason="Feature com recursos limitados!")
def test_comparacao_determinantes_5_matrizes_aleatorias_ordem_3():
    for execucao in range(5):
        A = MatrizBiDimensional([[random.uniform(-5,5) for i in range(3)] for i in range(3)])
        assert round(A.determinante(), 4) == round(wolfram_determinante(A), 4)

def test_excecao_matriz_singular():
    with pytest.raises(MatrizSingularException) as excinfo:
        a = MatrizBiDimensional([[1,2,3],\
                                 [4,5,6],\
                                 [7,8,9]])
        a.inversa()
    assert 'A matriz especificada é singular e não pode ser invertida!'

def test_private_inversa_por_fila_de_operacoes_elementares():
    A = MatrizBiDimensional([[1,2,3],\
                             [3,5,6],\
                             [7,1,9]])
    identidade = A * A._MatrizBiDimensional__inversa_por_fila_de_operacoes_elementares()
    for i in range(identidade.linhas):
        for j in range(identidade.colunas):
            identidade[i][j] = round(identidade[i][j], 0)
    assert identidade == MatrizBiDimensional.identidade(3)


def test_excecao_matriz_cofatores_nao_quadrada():
    with pytest.raises(MatrizInconsistenteException) as excinfo:
        a = MatrizBiDimensional([[1,2,3],\
                                 [4,5,6]])
        a.cofatores()
    assert 'A matriz especificada não é quadrada, portanto, não pode ter matriz de cofatores calculada!'

def test_matriz_adjunta():
    A = MatrizBiDimensional([[1,2,3],\
                             [3,5,6],\
                             [7,1,9]])
    assert A.adjunta() == MatrizBiDimensional([[39, -15, -3], [15, -12, 3], [-32, 13, -1]])

def test_private_inversa_por_adjunta_classica():
    A = MatrizBiDimensional([[1,2,3],\
                             [3,5,6],\
                             [7,1,9]])
    identidade = A * A._MatrizBiDimensional__inversa_por_adjunta_classica()
    for i in range(identidade.linhas):
        for j in range(identidade.colunas):
            identidade[i][j] = round(identidade[i][j], 0)
    assert identidade == MatrizBiDimensional.identidade(3)

def test_inversa_adjunta_classica_igual_inversa_fila_operacoes_elementares():
    A = MatrizBiDimensional([[1,2,3],\
                             [3,5,6],\
                             [7,1,9]])
    
    assert [[round(A.inversa(metodo_adjunta_classica=True)[i][j], 4) for j in range(3)] for i in range(3)] == [[round(A.inversa(metodo_adjunta_classica=False)[i][j], 4) for j in range(3)] for i in range(3)] 
