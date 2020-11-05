def construir_matriz_de_coeficientes(A, m): 
    matriz_de_indices = np.array([i for i in range(m ** 2)]).reshape(m, m) 
    coeficientes = np.zeros((m**2, m**2)) 
    for i in range(m ** 2): 
        j = int(i/m) 
        colunas = matriz_de_indices[:,i%m] 
        for k, l in zip(colunas, range(m)): 
            coeficientes[i][k] = A[j][l] 
    return coeficientes
