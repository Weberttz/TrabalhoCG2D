from Classes.plataforma import Plataforma
from Classes.zumbi import Zumbi
from Classes.cachorro import Cachorro
from Classes.pombo import Pombo
from Classes.coletavel import Coletavel
from settings import *
import csv

COR_ASFALTO, BORDA_ASFALTO = (74, 74, 74),   (44, 44, 48)
COR_CAIXA,   BORDA_CAIXA   = (178, 122, 66), (104, 66, 32)
COR_METAL,   BORDA_METAL   = (70, 130, 170), (36, 74, 104)
ROXO = (98, 0, 102)

# tile -> (cor, borda)
ESTILO_PLATAFORMA = {
    1: (COR_ASFALTO, BORDA_ASFALTO),
    2: (COR_CAIXA,   BORDA_CAIXA),
    3: (COR_METAL,   BORDA_METAL),
}

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
    imagem_seringa = pygame.image.load("Sprites/seringa.png").convert_alpha()
    imagem_tapioca = pygame.image.load("Sprites/tapioca.png").convert_alpha()
    imagem_municao = pygame.image.load("Sprites/municao.png").convert_alpha()
    imagem_fusivel = pygame.image.load("Sprites/fusivel.png").convert_alpha()
    imagem_moeda = pygame.image.load("Sprites/moeda.png").convert_alpha()
        
    plataformas, blocks, coletaveis = [], [], []
    T = TAMANHO_QUADRADO

    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            px, py = x * T, y * T

            match tile:
                case 1 | 2 | 3:
                    cor, borda = ESTILO_PLATAFORMA[tile]
                    plataformas.append(Plataforma(px, py, T, T, cor, borda))

                case 4:  # teleport
                    plataformas.append(
                        Plataforma(px, py, T, 2 * T, ROXO, BLACK, "teleport"))

                case 5:  # block
                    blocks.append(
                        Plataforma(px, py, T, T, AZUL_NOTURNO, BLACK, "block"))

                case 6:  # tapioca
                    raio = 16
                    coletaveis.append(Coletavel(Vetor(px, py + T // 2), raio, raio, WHITE, "tapioca", "circular", imagem_tapioca))

                case 7:  # moeda
                    coletaveis.append(
                        Coletavel(Vetor(px, py ), T, T, AMARELO, "moeda", "circular", imagem_moeda))

                case 8:  # munição
                    coletaveis.append(
                        Coletavel(Vetor(px, py), T, T, VERMELHO, "municao", imagem=imagem_municao))
                    
                case 9: # seringa
                    coletaveis.append(Coletavel(Vetor(px, py), T, T, VERMELHO, "especial", imagem=imagem_seringa))

                case 10: # fusível
                    coletaveis.append(Coletavel(Vetor(px, py), T, T, VERMELHO, "especial", imagem=imagem_fusivel))

                case _:  # 0 (vazio), 11-13 (inimigos/missão) e qualquer outro
                    pass

    return plataformas, blocks, coletaveis

def criar_inimigos(mapa, plataformas, blocks, nivel_dificuldade = None):
    zumbis = []
    cachorros = []
    pombos = []
    plats = [p for p in plataformas if p.tipo != "teleport"]

    for y, row in enumerate(mapa):
        for x, tile in enumerate(row):
            x_aux, y_aux = x * TAMANHO_QUADRADO, y * TAMANHO_QUADRADO - TAMANHO_QUADRADO

            match tile:
                case 11:
                    zumbi = Zumbi(plats + blocks, Vetor(x_aux, y_aux), [], (53, 66, 35), nivel_dificuldade)
                    zumbis.append(zumbi)
                case 12:
                    cachorro = Cachorro(plats + blocks, Vetor(x_aux, y_aux), [], (53, 66, 35), nivel_dificuldade)
                    cachorros.append(cachorro)
                case 13:
                    pombo = Pombo(plats + blocks, Vetor(x_aux, y_aux), (53, 66, 35), nivel_dificuldade)    
                    pombos.append(pombo)

    return zumbis, cachorros, pombos