import pygame
import sys

from BibliotecaGrafica.algoritmos import *
from Classes.plataforma import Plataforma
from Classes.jogador import Jogador
from Classes.zumbi import Zumbi
from Classes.camera import Camera
from Classes.arma import Arma
from random import randint
from Mapas.levelteste import level

BLACK = (0, 0, 0) # cor preta
WHITE = (255, 255, 255)
TAMANHO_QUADRADO = 30
QUANTIDADE_INIMIGOS = 20
LARGURA = 1262
ALTURA = 722
POS_INICIO = pygame.Vector2(100, 300)
VEL_ANIMACAO = 0.1

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

def criar_zumbis(plataformas):
    zumbis = []
    set_numeros = set()
    tamanho_zumbi = 30
    alocados = 0
    while alocados < QUANTIDADE_INIMIGOS:
        rnd = randint(0, len(plataformas) - 1)

        if rnd in set_numeros: continue

        x0, y1 = plataformas[rnd].x0, plataformas[rnd].y0 - tamanho_zumbi

        zumbi = Zumbi(plataformas, pygame.Vector2(x0, y1), [], (53, 66, 35))

        pode_alocar = True
        for plataforma in plataformas:
            if plataforma.retangulo.colliderect(zumbi.retangulo) and plataforma != plataformas[rnd]:
                pode_alocar = False
                break

        if not pode_alocar: continue

        zumbis.append(zumbi)
        set_numeros.add(rnd)
        alocados+=1

    return zumbis

def criar_level(layout):
    plataformas = []
    largura, altura = 30, 30
    cor_plataforma = (59, 132, 68)
    cor_marrom = (138, 51, 36)
    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            if tile == "P":
                plataforma = Plataforma(x * TAMANHO_QUADRADO,
                               y * TAMANHO_QUADRADO, largura, altura, cor_marrom)
                plataformas.append(plataforma)

    return plataformas

def gerar_lista_animacoes(nome, acao, tamanho):
    lista = []
    # Percorremos cada índice do menor que o tamanho da lista
    for i in range(tamanho):
        # Acrescentamos na lista cada imagem no formato indicado
        lista.append(f'{nome}_{acao}_{i}')

    return lista

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    clock = pygame.time.Clock()
    myriad_pro_font = pygame.font.SysFont("Myriad Pro", 30)

    pygame.display.set_caption("Jogo")
    rodando = True
    debug = True

    largura_mapa = len(level[0]) * TAMANHO_QUADRADO
    altura_mapa = len(level) * TAMANHO_QUADRADO

    plataformas = criar_level(level)
    zumbis = criar_zumbis(plataformas)
    
    arma = Arma(60, POS_INICIO.copy, "yellow")
    jogador = Jogador(POS_INICIO.copy(), plataformas, zumbis, [arma], BLACK)
    camera = Camera(jogador, largura_mapa, altura_mapa)
    tempo_animacao = 0

    # renderizar mundo na inicialização
    mundo_surface = pygame.Surface((largura_mapa, altura_mapa), pygame.SRCALPHA)
    for plataforma in plataformas:
        draw_polygonon(mundo_surface, plataforma.vertices, BLACK)
        scanline_fill(mundo_surface, plataforma.vertices, plataforma.cor)

    lista_zumbi_idle = gerar_lista_animacoes('zumbi', 'idle', 8)
    lista_zumbi_walk_left = gerar_lista_animacoes('zumbi', 'walk_left', 8)
    lista_zumbi_walk_right = gerar_lista_animacoes('zumbi', 'walk_right', 8)
            
    imagens_zumbi_idle = carregar_animacoes(lista_zumbi_idle)
    imagens_zumbi_walk_left = carregar_animacoes(lista_zumbi_walk_left)
    imagens_zumbi_walk_right = carregar_animacoes(lista_zumbi_walk_right)

    # Junta tudo e joga fora
    all_zumbis = imagens_zumbi_walk_right | imagens_zumbi_walk_left | imagens_zumbi_idle

    for z in zumbis:
        z.image = lista_zumbi_idle[0]

    while rodando:
        text = myriad_pro_font.render(f"Vida: {jogador.vida} ", 1, WHITE)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill(BLACK)

        if jogador.vida == 0 or jogador.pos.y > altura_mapa or jogador.pos.x > largura_mapa: 
            jogador.pos = POS_INICIO.copy()
            jogador.vida = 100
            
        jogador.atualizar()
        camera.atualizar()
        dx, dy = camera.camera.topleft  # offset atual da câmera

        zumbis_visiveis = [
            z for z in zumbis
            if -dx - z.tamanho <= z.pos.x <= -dx + LARGURA
        ]

        # A cada frame:
        tela.blit(mundo_surface, camera.camera.topleft)

        # imprimir jogador e arma
        vertices_jogador_tela = camera.aplicar_vertices(jogador.vertices)
        draw_polygonon(tela, vertices_jogador_tela, WHITE)
        scanline_fill(tela, vertices_jogador_tela, jogador.cor)
        vertices_arma_tela = camera.aplicar_vertices(jogador.equipamento.vertices)
        draw_polygonon(tela, vertices_arma_tela, jogador.equipamento.cor)
        scanline_fill(tela, vertices_arma_tela, WHITE)

        dt = clock.tick(60) / 1000
        tempo_animacao += dt
        avancar_frame = tempo_animacao >= VEL_ANIMACAO
        if avancar_frame:
            tempo_animacao = 0.0

        for zumbi in zumbis_visiveis:
            zumbi.atualizar()
            if avancar_frame:
                zumbi.animar(lista_zumbi_idle, lista_zumbi_walk_left, lista_zumbi_walk_right)

            vertices_na_tela = camera.aplicar_vertices(zumbi.vertices)

            imagem = all_zumbis.get(zumbi.image)

            if imagem is not None:
                pos_tela = vertices_na_tela[1]  # canto superior-esquerdo já com câmera aplicada
                tela.blit(pygame.transform.scale(imagem, (30, 30)), pos_tela)
            else:
                scanline_fill(tela, vertices_na_tela, zumbi.cor)
                draw_polygonon(tela, vertices_na_tela, "red")

        tela.blit(text, (30, 10))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()