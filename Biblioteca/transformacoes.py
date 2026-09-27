import math

def identidade():
    return [
        [1,0,0],
        [0,1,0],
        [0,0,1]
    ]

def produto_matriz(m,n):
    resultado = []
    linha = []

    if(len(m[0]) != len(n)):
        return None
    for i in range(len(m)): # linhas de m
        for j in range(len(n[0])):  # colunas de n
            item = 0
            for k in range(len(m[0])):
                item += m[i][k] * n[k][j]
            linha.append(item)
        resultado.append(linha)
        linha = []
    if(len(n[0]) == 1):
        resultado = [resultado[i][0] for i in range(len(resultado) - 1)]
        
    return resultado 
# com a 2x2 só conseguimos realizar transformações lineares(rotação,escala,cisalhamento)
# a coluna e a linha a mais existe para possibilitar o uso de uma matriz na translação
# e com a linha a mais usamos o 1 e o 0 para diferer o pivo do vetor 
# de modo que um pivo(1) pode ser transladado, mas um vetor(0) não 
def translacao(x, y): # vetor deslocamento (movimento no eixo x e no eixo y)
    return[
        [1,0,x],
        [0,1,y],
        [0,0,1]
    ]
def escala (x,y):
    return[
        [x,0,0],
        [0,y,0],
        [0,0,1]
    ]
# rotacao em torno do eixo z
def rotacao(angulo):
    c = math.cos(angulo)
    s = math.sin(angulo)
    return [
        [c,-s,0],
        [s,c,0],
        [0,0,1]
    ]     

def safty_escala(x,y,pivo):
    translacao_origem = translacao(-pivo[0],-pivo[1])
    escala_origem = escala(x,y)
    translacao_volta = translacao(pivo[0],pivo[1])
    matriz_escala = produto_matriz(translacao_origem,escala_origem)
    matriz_escala = produto_matriz(matriz_escala,translacao_volta)

    return matriz_escala

def safty_rotacao(x,y,pivo): # gera a matriz para ser aplicada nos pontos e usa apenas um como pivo
    translacao_origem = translacao(-pivo[0],-pivo[1])
    rotacao_origem = rotacao(x,y)
    translacao_volta = translacao(pivo[0],pivo[1])
    matriz_rotacao = produto_matriz(translacao_origem,rotacao_origem)
    matriz_rotacao = produto_matriz(matriz_rotacao,translacao_volta)

    return matriz_rotacao
