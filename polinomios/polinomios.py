import numpy as np

def p_de_A(coeficientes, A):
    pA = np.zeros(A.shape, dtype='complex128')
    for i, j in zip(range(len(coeficientes)), reversed(range(len(coeficientes)))):
        pA += coeficientes[i] * np.linalg.matrix_power(A, j)
    return pA
