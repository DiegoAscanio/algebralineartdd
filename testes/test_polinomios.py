from polinomios.polinomios import p_de_A
import numpy as np

def test_p_de_A():
    A = np.array([[-1, 4], [2, 1]])
    p = [1, 0, -9]
    assert np.allclose(p_de_A(p, A), np.zeros((2,2)))

def test_q_de_A():
    A = np.array([[-1, 4], [2, 1]])
    q = [2, 3]
    assert np.allclose(p_de_A(q, A), np.array([[1, 8], [4, 5]]))

