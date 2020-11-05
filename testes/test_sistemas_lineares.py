import pytest
import random
import copy

from sistemas_lineares.sistemas_lineares import SL
from sistemas_lineares.exceptions import SLInvalidoException, SLInsolucionavelException
from matriz.matriz import MatrizBiDimensional
#from testes.utils import wolfram_escalonamento_linha_reduzido, wolfram_determinante

def test_excecao_instanciar_sistema_linear_tipo_invalido():
    with pytest.raises(SLInvalidoException) as excinfo:
        sl = SL([[0,1],[1,0]], MatrizBiDimensional([[1],[2]]))
    assert 'Coeficientes e/ou Termos Independentes Inválidos! Os coeficientes e termos independente devem ser do tipo MatrizBiDimensional; O numero de linhas da matriz de coeficientes deve ser igual ao número de linhas da matriz de termos independentes; A matriz de termos independentes deve ser uma matriz coluna' in str(excinfo.value)


def test_excecao_instanciar_sistema_linear_numero_linhas_coeficientes_diferente_numero_linhas_termos_independentes():
    with pytest.raises(SLInvalidoException) as excinfo:
        sl = SL(MatrizBiDimensional([[0,1],[1,0]]), MatrizBiDimensional([[1]]))
    assert 'Coeficientes e/ou Termos Independentes Inválidos! Os coeficientes e termos independente devem ser do tipo MatrizBiDimensional; O numero de linhas da matriz de coeficientes deve ser igual ao número de linhas da matriz de termos independentes; A matriz de termos independentes deve ser uma matriz coluna' in str(excinfo.value)


def test_excecao_instanciar_sistema_linear_matriz_termos_independentes_linha():
    with pytest.raises(SLInvalidoException) as excinfo:
        sl = SL(MatrizBiDimensional([[0,1],[1,0]]), MatrizBiDimensional([[1, 2]]))
    assert 'Coeficientes e/ou Termos Independentes Inválidos! Os coeficientes e termos independente devem ser do tipo MatrizBiDimensional; O numero de linhas da matriz de coeficientes deve ser igual ao número de linhas da matriz de termos independentes; A matriz de termos independentes deve ser uma matriz coluna' in str(excinfo.value)

def test_igualdade_sistemas_lineares():
    sl_1 = SL(MatrizBiDimensional([[0,1],[1,0]]), MatrizBiDimensional([[1], [2]]))
    sl_2 = SL(MatrizBiDimensional([[0,1],[1,0]]), MatrizBiDimensional([[1], [2]]))
    assert sl_1 == sl_2

def test_property_numero_incognitas():
    sl = SL(MatrizBiDimensional([[0,1],[1,0]]), MatrizBiDimensional([[1], [2]]))
    assert sl.incognitas == 2

def test_property_numero_equacoes():
    sl = SL(MatrizBiDimensional([[0,1],[1,0]]), MatrizBiDimensional([[1], [2]]))
    assert sl.equacoes == 2

def test_private_matriz_aumentada():
    sl = SL(MatrizBiDimensional([[0,1],[1,0]]), MatrizBiDimensional([[1], [2]]))
    assert sl._SL__matriz_aumentada() == MatrizBiDimensional([[0,1,1],[1,0,2]])

def test_sistema_solucionavel():
    sl = SL(MatrizBiDimensional([[0,1],[1,0]]), MatrizBiDimensional([[1], [2]]))
    assert sl.solucionavel == True

def test_sistema_nao_solucionavel():
    sl = SL(MatrizBiDimensional([[1,1],[1,1]]), MatrizBiDimensional([[1], [2]]))
    assert sl.solucionavel == False

def test_excecao_resolver_sistema_insolucionavel():
    with pytest.raises(SLInsolucionavelException) as excinfo:
        sl = SL(MatrizBiDimensional([[1,1],[1,1]]), MatrizBiDimensional([[1], [2]]))
        sl.resolver()
    assert 'O sistema especificado não possui solução' in str(excinfo.value)

def test_private_matriz_coeficientes_quadrada():
    sl = SL(MatrizBiDimensional([[1, 2],[1, -1]]), MatrizBiDimensional([[3],[5]]))
    assert sl._SL__matriz_coeficientes_quadrada() == True

def test_private_matriz_coeficientes_nao_quadrada():
    sl = SL(MatrizBiDimensional([[1, 2]]), MatrizBiDimensional([[3]]))
    assert sl._SL__matriz_coeficientes_quadrada() == False

def test_private_aplicar_forma_linha_reduzida_para_construir_matriz_solucao():
    sl = SL(MatrizBiDimensional([[1, 2],[1, -1]]), MatrizBiDimensional([[3],[5]]))
    sl._SL__aplicar_forma_linha_reduzida_para_construir_matriz_solucao()
    assert sl._SL__matriz_solucao == MatrizBiDimensional([[1.0, 0.0, 4.333333333333333], [0.0, 1.0, -0.6666666666666666]])
def test_private_separar_coeficientes_termos_independentes_matriz_solucao():
    sl = SL(MatrizBiDimensional([[1, 2],[1, -1]]), MatrizBiDimensional([[3],[5]]))
    sl._SL__aplicar_forma_linha_reduzida_para_construir_matriz_solucao()
    sl._SL__separar_coeficientes_termos_independentes_matriz_solucao()
    assert (sl._SL__coeficientes_matriz_solucao, sl._SL__termos_independentes_matriz_solucao) == (MatrizBiDimensional.identidade(2), MatrizBiDimensional([[13/3], [-2/3]]))
def test_private_solucao_forma_escada_linha_reduzida():
    sl = SL(MatrizBiDimensional([[1, 2],[1, -1]]), MatrizBiDimensional([[3],[5]]))
    assert sl._SL__solucao_forma_escada_linha_reduzida() == {0: (13/3, [(1, 0)]), 1: (-2/3, [(0, 0)])}

def test_private_str_solucao_forma_escada_linha_reduzida():
    sl = SL(MatrizBiDimensional([[1, 2],[1, -1]]), MatrizBiDimensional([[3],[5]]))
    sl._SL__solucao_forma_escada_linha_reduzida()
    assert sl._SL__str_solucao() == 'X_0 = 4.333333333333333\nX_1 = -0.6666666666666666\n'

def test_private_str_solucao_forma_escada_linha_reduzida_sistema_nao_determinado():
    sl = SL(MatrizBiDimensional([[1, 0, 3, 2],[1, -1, 0, 0],[0, 12, 0, 0]]), MatrizBiDimensional([[3],[5],[13]]))
    sl._SL__solucao_forma_escada_linha_reduzida()
    assert sl._SL__str_solucao() == 'X_0 = 6.083333333333333\nX_1 = 1.083333333333333\nX_2 = -1.0277777777777777 -0.6666666666666666X_3\n'

def test_private_solucao_regra_crammer():
    sl = SL(MatrizBiDimensional([[1, 2],[1, -1]]), MatrizBiDimensional([[3],[5]]))
    assert sl._SL__solucao_regra_crammer() == {0: (13/3, []), 1: (-2/3, [])}

def test_private_str_solucao_regra_crammer():
    sl = SL(MatrizBiDimensional([[1, 2],[1, -1]]), MatrizBiDimensional([[3],[5]]))
    sl._SL__solucao_regra_crammer()
    assert sl._SL__str_solucao() == 'X_0 = 4.333333333333333\nX_1 = -0.6666666666666666\n'
