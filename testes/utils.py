import wolframalpha

from matriz.matriz import MatrizBiDimensional

f = open('testes/wolfram-app-id.txt')
app_id = f.readline().replace('\n', '')
f.close()
client = wolframalpha.Client(app_id)

def __adicionar_linha_a_query(matriz, i):
    return '{' + ','.join([ str(matriz[i][j]) for j in range(matriz.colunas) ]) + '}'

def __produzir_determinante_a_partir_de_wolfram_subpod(subpod):
    return float(subpod['plaintext'])

def __produzir_matriz_bi_dimensional_a_partir_de_wolfram_subpod(subpod):
    resultado_wolfram = subpod['plaintext'].replace('(', '').replace(')', '').replace('|',',').replace(' ','')
    return MatrizBiDimensional([ [float(numero) if len(numero.split('/')) != 2 else float(numero.split('/')[0]) / float(numero.split('/')[1]) for numero in linha.split(',')] for linha in resultado_wolfram.split('\n') ])

def wolfram_determinante(matriz):
    query = 'determinant of {' + ','.join([ __adicionar_linha_a_query(matriz, i) for i in range(matriz.linhas) ]) + '}'
    resposta = client.query(query)
    for pod in resposta.pods:
        if pod['@title'] == 'Result':
            return __produzir_determinante_a_partir_de_wolfram_subpod(pod['subpod'])

def wolfram_escalonamento_linha_reduzido(matriz):
    query = 'reduced row echelon form {' + ','.join([ __adicionar_linha_a_query(matriz, i) for i in range(matriz.linhas) ]) + '}'
    resposta = client.query(query)
    for pod in resposta.pods:
        if pod['@title'] == 'Result':
            return __produzir_matriz_bi_dimensional_a_partir_de_wolfram_subpod(pod['subpod'])
