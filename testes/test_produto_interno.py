import pytest
import random
import copy
import numpy as np

from produto_interno.produto_interno import norma, produto_interno_canonico, produto_interno, angulo, projecao_escalar, projecao_vetorial, v_ortogonal_u, normalizar, gram_schmidt, ortogonalizar_vetores, normalizar_vetores, ortonormalizar_vetores

def test_norma_1_r1():
    assert norma(np.array([1])) == 1

def test_norma_2_r1():
    assert norma(np.array([2])) == 2

def test_norma_0_1_r1():
    assert norma(np.array([0, 1])) == np.linalg.norm(np.array([0, 1]))

def test_produto_interno_canonico_1_r1_1_r1():
    u = np.array([1])
    v = np.array([1])
    assert produto_interno_canonico(u, v) == np.inner(u, v)

def test_produto_interno_canonico_2_r1_7_r1():
    u = np.array([2])
    v = np.array([7])
    assert produto_interno_canonico(u, v) == np.inner(u, v)

def test_produto_interno_canonico_r2_aleatorios():
    u = np.random.randint(10, size=2)
    v = np.random.randint(10, size=2)
    assert produto_interno_canonico(u, v) == np.inner(u, v)

def test_produto_interno_canonico_rn_aleatorios():
    n = np.random.randint(100000, size=1)
    u = np.random.randint(n, size=2)
    v = np.random.randint(n, size=2)
    assert produto_interno_canonico(u, v) == np.inner(u, v)

def test_produto_interno_nao_canonico_r2():
    u = np.array([5, 2])
    v = np.array([-2, 3])
    funcional_linear = lambda u, v: 2*u[0]*v[0] + u[0]*v[1] + u[1]*v[0] + u[1]*v[1]
    assert produto_interno(u, v, funcional_linear = funcional_linear) == -3

def test_norma_canonica_r2():
    u = np.array([2**0.5, 0])
    assert norma(u) == 2**(0.5)

def test_norma_nao_canonica_r2():
    u = np.array([2**0.5, 0])
    funcional_linear = lambda u, v: 2*u[0]*v[0] + u[0]*v[1] + u[1]*v[0] + u[1]*v[1]
    assert norma(u, funcional_linear = funcional_linear) == 2

def test_angulo_dois_vetores_ortogonais_r2():
    u = np.array([0, 1])
    v = np.array([1, 0])
    assert angulo(u, v) == np.arccos(0)

def test_angulo_dois_vetores_nao_ortogonais_r2():
    u = np.array([1, 0])
    v = np.array([1, 3**0.5])
    assert np.allclose(angulo(u, v), np.arccos(0.5))

def test_angulo_produto_interno_nao_canonico_r2():
    funcional_linear = lambda u, v: 2*u[0]*v[0] + u[0]*v[1] + u[1]*v[0] + u[1]*v[1]
    u = np.array([2**0.5, 0])
    v = np.array([2**0.5, 0])
    assert np.allclose(angulo(u, v, funcional_linear = funcional_linear), np.arccos(1))

def test_projecao_escalar_u_v_ortogonais_r2():
    u = np.array([1, 0])
    v = np.array([0, 1])
    assert projecao_escalar(u, v) == 0

def test_projecao_escalar_u_v_paralelos_r2():
    u = np.array([1, 0])
    v = 2*u
    assert projecao_escalar(u, v) == 1

def test_projecao_vetorial_u_v_ortogonais_r2():
    u = np.array([1, 0])
    v = np.array([0, 1])
    assert np.allclose(projecao_vetorial(u, v), np.zeros(u.shape))

def test_projecao_escalar_u_v_paralelos_r2():
    u = np.array([1, 0])
    v = 2*u
    assert np.allclose(projecao_vetorial(u, v), u)


def test_projecao_vetorial_u_v_produto_interno_nao_canonico_r2():
    funcional_linear = lambda u, v: 2*u[0]*v[0] + u[0]*v[1] + u[1]*v[0] + u[1]*v[1]
    u = np.array([1, 1])
    v = np.array([0, 1])
    assert np.allclose(projecao_vetorial(u, v, funcional_linear = funcional_linear), 2*v)

def test_v_ortogonal_u():
    u = np.array([1, 1])
    v = np.array([0, 1])
    assert np.allclose(v_ortogonal_u(u, v), np.array([-1/2, 1/2]))

def test_v_ortogonal_u_produto_interno_nao_canonico_r2():
    funcional_linear = lambda u, v: 2*u[0]*v[0] + u[0]*v[1] + u[1]*v[0] + u[1]*v[1]
    u = np.array([1, 1])
    v = np.array([0, 1])
    assert np.allclose(v_ortogonal_u(u, v, funcional_linear = funcional_linear), np.array([-2/5, 3/5]))

def test_normalizar_u():
    u = np.array([1, 1])
    assert np.allclose(normalizar(u), np.array([(2**0.5)/2, (2**0.5)/2]))


def test_normalizar_u_produto_interno_nao_canonico_r2():
    funcional_linear = lambda u, v: 2*u[0]*v[0] + u[0]*v[1] + u[1]*v[0] + u[1]*v[1]
    u = np.array([1, 0])
    assert np.allclose(normalizar(u, funcional_linear = funcional_linear), np.array([(2**0.5)/2, 0]))

def test_gram_schmidt_v_r3():
    u = np.array([1, 1, 0])
    v = np.array([1, 0, 1])
    w = np.array([0, 2, 0])
    base = [u, v, w]
    assert np.allclose(gram_schmidt(1, base), np.array([1/2, -1/2, 1]))

def test_ortogonalizar_vetores():
    u, u_ortog = np.array([1, 1, 0]), np.array([1, 1, 0])
    v, v_ortog = np.array([1, 0, 1]), np.array([1/2, -1/2, 1])
    w, w_ortog = np.array([0, 2, 0]), np.array([-2/3, 2/3, 2/3])
    base = [u, v, w]
    base_ortogonal = [u_ortog, v_ortog, w_ortog]
    assert np.allclose(ortogonalizar_vetores(base), base_ortogonal)

def test_normalizar_vetores():
    u, u_norm = np.array([1, 1, 0]), np.array([1/2**0.5, 1/2**0.5, 0])
    v, v_norm = np.array([1, 0, 1]), np.array([1/2**0.5, 0, 1/2**0.5])
    w, w_norm = np.array([0, 2, 0]), np.array([0, 1, 0])
    vetores = [u, v, w]
    normalizados = [u_norm, v_norm, w_norm]
    assert np.allclose(normalizar_vetores(vetores), normalizados)

def test_ortonormalizar_vetores():
    u, u_orton = np.array([1, 1, 0]), np.array([1/2**0.5, 1/2**0.5, 0])
    v, v_orton = np.array([1, 0, 1]), np.array([1/6**0.5, -1/6**0.5, 2/6**0.5])
    w, w_orton = np.array([0, 2, 0]), np.array([-1/3**0.5, 1/3**0.5, 1/3**0.5])
    base = [u, v, w]
    base_ortonormal = [u_orton, v_orton, w_orton]
    assert np.allclose(ortonormalizar_vetores(base), base_ortonormal)

def test_ortonormalizar_vetores_polinomiais():
    u = np.polynomial.Polynomial([0, 0, 1]) # u = 1 * t^2 
    v = np.polynomial.Polynomial([0, 1])    # v = 1 * t
    w = np.polynomial.Polynomial([1])       # w = 1
    u_ortn = np.polynomial.Polynomial([0, 0, 1/2**0.5]) # u_ortn = 1/2^0.5 * t^2
    v_ortn = np.polynomial.Polynomial([0, 1/2**0.5])    # v_ortn = 1/2^0.5 * t
    w_ortn = np.polynomial.Polynomial([1,    0,    -1]) # w_ortn = -1 * t^2 - 1
    base = [u, v, w]
    base_ortonormal = [u_ortn, v_ortn, w_ortn]

    produto_interno_polinomial = lambda p, q: p(-1) * q(-1) + p(0) * q(0) + p(1) * q(1)
    base_ortonormal_calculada = ortonormalizar_vetores(base, funcional_linear = produto_interno_polinomial)

    assert base_ortonormal_calculada == base_ortonormal
