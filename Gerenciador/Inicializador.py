from Classes.plataforma import Plataforma
from Classes.zumbi import Zumbi
from Classes.cachorro import Cachorro
from Classes.coletavel import Coletavel
from settings import *
from random import randint
import csv

def carregar_animacoes(lista_nomes, pasta="Sprites"):
    """Recebe uma lista de nomes (ex: 'zumbi_idle_0') e devolve um dicionário
    nome -> pygame.Surface já carregada."""
    imagens = {}
    for nome in lista_nomes:
        caminho = f"{pasta}/{nome}.png"
        try:
            imagens[nome] = pygame.image.load(caminho).convert_alpha()
        except pygame.error as e:
            print(f"Não consegui carregar '{caminho}': {e}")
    return imagens
 
def gerar_lista_animacoes(nome, acao, tamanho):
    return [f"{nome}_{acao}_{i}" for i in range(tamanho)]
 
def carregar_mapa(nome_arquivo):
    """Ler o arquivo .csv e recolhe todas as  linhas, adiciona cada numero da linha em mapa"""
    mapa = []
    with open(nome_arquivo, "r") as f:
        for linha in csv.reader(f):
            mapa.append([int(bloco) for bloco in linha])
    return mapa
 
def criar_level(layout):
    cores = [None, MARROM, VERDE, AMARELO, WHITE, AZUL_NOTURNO]
    plataformas = []
    blocks = []
    coletaveis = []
    largura, altura = 30, 30

    # 1, 2, 3, 4 são plataformas - 4 vai ser teleport - usar gradiente
    # 5 é block
    # 6, 7, 8 são coletáveis

    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            if tile == 5:
                block = Plataforma(x * TAMANHO_QUADRADO, y * TAMANHO_QUADRADO, largura, altura, cores[tile])
                blocks.append(block)
            elif tile == 6:
                tapioca = Coletavel(Vetor(x * TAMANHO_QUADRADO, y * TAMANHO_QUADRADO), 10, WHITE, "tapioca")
                coletaveis.append(tapioca)
            elif tile == 7:
                coletavel = Coletavel(Vetor(x * TAMANHO_QUADRADO, y * TAMANHO_QUADRADO + 16), 8, AMARELO, "moeda")
                coletaveis.append(coletavel)
            elif tile == 8:
                coletavel = Coletavel(Vetor(x * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, 
                                            y * TAMANHO_QUADRADO), 10, VERMELHO, "municao")
                coletaveis.append(coletavel)
            elif tile != 0:
                plataforma = Plataforma(x * TAMANHO_QUADRADO, y * TAMANHO_QUADRADO, largura, altura, cores[tile])
                plataformas.append(plataforma) 

    return plataformas, blocks, coletaveis

def criar_zumbis(plataformas, blocks, max_tentativas=1000):
    zumbis = []
    usadas = set()
    tamanho_zumbi = 30
    tentativas = 0

    while len(zumbis) < QUANTIDADE_INIMIGOS // 2 and tentativas < max_tentativas:
        tentativas += 1
        rnd = randint(0, len(plataformas) - 1)
        if rnd in usadas:
            continue

        x0, y1 = plataformas[rnd].x0,  plataformas[rnd].y0 - tamanho_zumbi
        zumbi = Zumbi(plataformas + blocks, Vetor(x0, y1), [], (53, 66, 35))

        # não pode nascer dentro de outra plataforma
        if any(p.retangulo.colidiu_com(zumbi.retangulo) and p != plataformas[rnd]
               for p in plataformas):
            continue

        zumbis.append(zumbi)
        usadas.add(rnd)

    return zumbis

def criar_cachorros(plataformas, blocks, max_tentativas=1000):
    cachorros = []
    usadas = set()
    tamanho_cachorros = 30
    tentativas = 0
    
    while len(cachorros) < QUANTIDADE_INIMIGOS // 2 and tentativas < max_tentativas:
        tentativas += 1
        rnd = randint(0, len(plataformas) - 1)
        if rnd in usadas:
            continue

        x0, y1 = plataformas[rnd].x0,  plataformas[rnd].y0 - tamanho_cachorros
        cachorro = Cachorro(plataformas + blocks, Vetor(x0, y1), [], (53, 66, 35))

        # não pode nascer dentro de outra plataforma
        if any(p.retangulo.colidiu_com(cachorro.retangulo) and p != plataformas[rnd]
            for p in plataformas):
            continue

        cachorros.append(cachorro)
        usadas.add(rnd)

    return cachorros