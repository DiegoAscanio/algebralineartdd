import numpy as np

def multiplicar_matrizes(A, B):
    def somatorio(i, j):
        expressao = 'r['+ str(int(i + 1)) + ', ' + str(int(j + 1)) + ']=\t'
        r = 0
        for k in range(len(A[i])):
            expressao += '(' + str(int(A[i][k])) + '*' + str(int(B[k][j])) + ')'
            if k < len(A[i]) - 1:
                expressao += ' +\t'
            r += A[i][k] * B[k][j]
        return r, expressao
    # se o numero de colunas da matriz A
    # for diferente do numero de linhas
    # da matriz B, a multiplicacao nao
    # pode ser realizada
    if len(A[0]) != len(B):
        raise Exception('As dimensões das matrizes são incompatíveis')
    resultado = '\t\tai1b1j\tai2b2j\tai3b3j\tai4b4j\tai5b5j\n'
    R = np.array([[0 for i in range(len(B[-1]))] for j in range(len(A))]) 
    for l in range(len(A)):
        for c in range(len(B[-1])):
            r, expressao = somatorio(l, c)
            R[l][c] = r
            resultado += expressao + ' = ' + str(int(r)) + '\n'
    return R, resultado

A = np.array([[0, 1, 1, 1, 1],[1, 0, 1, 1, 0],[0, 1, 0, 1, 0],[0, 0, 1, 0, 1],[0, 0, 0, 1, 0]])
A2, expansao = multiplicar_matrizes(A, A)

print('AxA\n' + str(A2) + '\n')
print('\t\tSomatórios Realizados\n\n' + expansao)
