import pygame
import sys

from BibliotecaGrafica.algoritmos import *
from Classes.plataforma import Plataforma
from Classes.jogador import Jogador
from Classes.zumbi import Zumbi
from Classes.camera import Camera
from random import randint
from Mapas.level import level

BLACK = (0, 0, 0) # cor preta
WHITE = (255, 255, 255)
TAMANHO_QUADRADO = 30
QUANTIDADE_INIMIGOS = 5
LARGURA = 1262
ALTURA = 722

def criar_zumbis(plataformas):
    zumbis = []
    set_numeros = set()
    tamanho_zumbi = 30
    distancia = 5
    alocados = 0
    while alocados < QUANTIDADE_INIMIGOS:
        rnd = randint(0, len(plataformas) - 1)

        if rnd in set_numeros: continue

        x0, y1 = plataformas[rnd].x0, plataformas[rnd].y0 - tamanho_zumbi

        zumbi = Zumbi(plataformas, pygame.Vector2(x0, y1), (53, 66, 35))

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
    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            if tile == "P":
                plataforma = Plataforma(x * TAMANHO_QUADRADO,
                               y * TAMANHO_QUADRADO, largura, altura, (59, 132, 68))
                plataformas.append(plataforma)

    return plataformas

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
    jogador = Jogador(plataformas, zumbis, "red")

    camera = Camera(jogador, largura_mapa, altura_mapa)

    # renderizar mundo na inicialização
    mundo_surface = pygame.Surface((largura_mapa, altura_mapa), pygame.SRCALPHA)
    for plataforma in plataformas:
        draw_polygonon(mundo_surface, plataforma.vertices, BLACK)
        scanline_fill(mundo_surface, plataforma.vertices, plataforma.cor)

    while rodando:
        text = myriad_pro_font.render(f"Vida: {jogador.vida} ", 1, WHITE)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill(BLACK)
        jogador.atualizar()
        camera.atualizar()
        dx, dy = camera.camera.topleft  # offset atual da câmera

        zumbis_visiveis = [
            z for z in zumbis
            if -dx - z.tamanho <= z.pos.x <= -dx + LARGURA
        ]

        # A cada frame:
        tela.blit(mundo_surface, camera.camera.topleft)

        vertices_jogador_tela = camera.aplicar_vertices(jogador.vertices)
        draw_polygonon(tela, vertices_jogador_tela, jogador.cor)

        for zumbi in zumbis_visiveis:
            if debug: print(f"x0 = {zumbi.pos.x}")
            zumbi.atualizar()
            vertices_na_tela = camera.aplicar_vertices(zumbi.vertices)
            draw_polygonon(tela, vertices_na_tela, "red")
            scanline_fill(tela, vertices_na_tela, zumbi.cor)

        debug = False

        tela.blit(text, (30, 10))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()