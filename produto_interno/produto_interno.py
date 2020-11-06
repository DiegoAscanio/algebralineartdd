import pdb
import numpy as np

def produto_interno_canonico(u, v):
    resultado = 0
    for i in range(len(u)):
        resultado += u[i] * v[i]
    return resultado

def produto_interno(u, v, funcional_linear = produto_interno_canonico):
    return funcional_linear(u, v)

def norma(v, funcional_linear = produto_interno_canonico):
    return funcional_linear(v, v) ** (0.5)

def angulo(u, v, funcional_linear = produto_interno_canonico):
    return np.arccos(np.around(funcional_linear(u, v) / (norma(u, funcional_linear = funcional_linear) * norma(v, funcional_linear = funcional_linear)), decimals = 6))

def projecao_escalar(u, v, funcional_linear = produto_interno_canonico):
    return np.around(produto_interno(u, v, funcional_linear = funcional_linear)\
         / produto_interno(v, v, funcional_linear = funcional_linear), decimals = 6)

def projecao_vetorial(u, v, funcional_linear = produto_interno_canonico):
    return projecao_escalar(u, v, funcional_linear = funcional_linear) * v

def v_ortogonal_u(u, v, funcional_linear = produto_interno_canonico):
    return v - projecao_escalar(v, u, funcional_linear = funcional_linear) * u

def normalizar(u, funcional_linear = produto_interno_canonico):
    return u / norma(u, funcional_linear = funcional_linear)

def gram_schmidt(i, vetores, funcional_linear = produto_interno_canonico):
    w = [vetores[0]]
    for j in range(1, i + 1):
        v = vetores[j]
        w += [v - sum([projecao_vetorial(v, w[k], funcional_linear = funcional_linear) for k in range(j)])]
    return w[i]

def ortogonalizar_vetores(vetores, funcional_linear = produto_interno_canonico):
    ortogonalizados = []
    for i in range(len(vetores)):
        ortogonalizados += [gram_schmidt(i, vetores, funcional_linear = funcional_linear)]
    return ortogonalizados

def normalizar_vetores(vetores, funcional_linear = produto_interno_canonico):
    normalizados = []
    for v in vetores:
        normalizados += [normalizar(v, funcional_linear = funcional_linear)]
    return normalizados

def ortonormalizar_vetores(vetores, funcional_linear = produto_interno_canonico):
    return normalizar_vetores(ortogonalizar_vetores(vetores, funcional_linear = funcional_linear), funcional_linear = funcional_linear)
