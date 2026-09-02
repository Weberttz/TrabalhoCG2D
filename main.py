import pygame
import sys

from bresenham import linha_bresenham
from plataforma import Plataforma
from jogador import Jogador
from zumbi import Zumbi
from random import randint
from level import level

cor_preta = (0, 0, 0) # cor preta
cor_branca = (255, 255, 255)
TAMANHO_QUADRADO = 30

def set_pixel(superficie, x, y, cor):
    superficie.set_at((x,y), cor)

def draw_line(superficie, pontos, cor):
    for (x, y) in pontos:
        set_pixel(superficie, x, y, cor)

def draw_polygonon(superficie, vertices, color):
    n = len(vertices)
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i+1) % n]
        linha_bresenham(superficie, x0, y0, x1, y1, color)

def criar_zumbi(plataformas):
    rnd = randint(0, len(plataformas))
    tamanho_zumbi = 30
    return Zumbi(plataformas[rnd].x1 - tamanho_zumbi, plataformas[rnd].y1)

def criar_level(layout):
    plataformas = []
    largura, altura = 30, 30
    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            if tile == "P":
                plataforma = Plataforma(x * TAMANHO_QUADRADO, x * TAMANHO_QUADRADO + largura,
                               y * TAMANHO_QUADRADO, y * TAMANHO_QUADRADO + altura, cor_branca)
                plataformas.append(plataforma)

    return plataformas

def main():
    pygame.init()
    largura, altura = 1280, 720
    tela = pygame.display.set_mode((largura, altura))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Jogo")
    rodando = True

    plataformas = criar_level(level)
    jogador = Jogador(plataformas, "red")

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
        
        jogador.atualizar()
        tela.fill(cor_preta)

        for plataforma in plataformas:
            draw_polygonon(tela, plataforma.vertices, plataforma.cor)

        draw_polygonon(tela, jogador.vertices, jogador.cor)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()