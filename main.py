import pygame
import sys

from BibliotecaGrafica.algoritmos import *
from Classes.plataforma import Plataforma
from Classes.jogador import Jogador
from Classes.zumbi import Zumbi
from random import randint
from Mapas.level import level

BLACK = (0, 0, 0) # cor preta
WHITE = (255, 255, 255)
TAMANHO_QUADRADO = 30
QUANTIDADE_INIMIGOS = 5

def criar_zumbis(plataformas):
    zumbis = []
    set_numeros = set()
    tamanho_zumbi = 30
    distancia = 5
    for _ in range(QUANTIDADE_INIMIGOS):
        rnd = randint(0, len(plataformas))

        if rnd + distancia > len(plataformas): continue

        for i in range(rnd, rnd + distancia):
            if i in set_numeros: continue

        zumbis.append(Zumbi(plataformas[rnd].x0, plataformas[rnd].y1 - tamanho_zumbi, 
                    tamanho_zumbi, tamanho_zumbi, (53, 66, 35)))
        set_numeros.add(rnd)

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
    largura, altura = 1262, 722
    tela = pygame.display.set_mode((largura, altura))
    clock = pygame.time.Clock()
    myriad_pro_font = pygame.font.SysFont("Myriad Pro", 30)

    pygame.display.set_caption("Jogo")
    rodando = True

    plataformas = criar_level(level)
    zumbis = criar_zumbis(plataformas)
    jogador = Jogador(plataformas, zumbis, "red")

    while rodando:
        text = myriad_pro_font.render(f"Vida: {jogador.vida} ", 1, WHITE)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if jogador.pos.y > altura or jogador.vida == 0: 
            jogador.pos.y = 40
            jogador.vida = 100

        jogador.atualizar()
        tela.fill(BLACK)

        for plataforma in plataformas:
            draw_polygonon(tela, plataforma.vertices, BLACK)
            scanline_fill(tela, plataforma.vertices, plataforma.cor)

        draw_polygonon(tela, jogador.vertices, jogador.cor)

        for zumbi in zumbis:
            zumbi.atualizar()
            draw_polygonon(tela, zumbi.vertices, BLACK)
            scanline_fill(tela, zumbi.vertices, zumbi.cor)

        tela.blit(text, (30, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()