import pygame
import sys

from bresenham import linha_bresenham
from plataforma import Plataforma
from jogador import Jogador

pygame.init()
largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()

cor_preta = (0, 0, 0) # cor preta
cor_branca = (255, 255, 255)

pygame.display.set_caption("Jogo")
rodando = True

jogador = Jogador("red")
dt = 0
gravidade = 4

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

def criar_plataformas():
    plataformas = []
    x0, y0 = 0, 718
    largura, altura = 100, 28
    distancia = 60
    for _ in range(4):
        x1 = x0 + largura
        y1 = y0 - altura
        
        plataforma = Plataforma(x0, x1, y0, y1, cor_branca)
        plataformas.append(plataforma)
        x0+=largura + distancia

    return plataformas

def aplicar_gravidade(jogador):
    jogador.y += jogador.vel

    if jogador.y >= altura: 
        jogador.y = altura
        jogador.y = 0

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    print(pygame.mouse.get_pos())
    tela.fill(cor_preta)

    vertices = [(jogador.x, jogador.y), 
                (jogador.x + jogador.tamanho, jogador.y), 
                (jogador.x + jogador.tamanho, jogador.y - jogador.tamanho), 
                (jogador.x, jogador.y - jogador.tamanho)]
    
    draw_polygonon(tela, vertices,jogador.cor)

    plataformas = criar_plataformas()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and jogador.no_chao:
       jogador.y -= jogador.vel  
       jogador.no_chao = False

    if keys[pygame.K_LEFT]:
        jogador.x -= jogador.vel
    if keys[pygame.K_RIGHT]:
        jogador.x += jogador.vel

    pode_cair = True

    for plataforma in plataformas:
        for (x, y) in plataforma.vertices:
            valor1 = plataforma.x0 - jogador.tamanho
            valor2 = plataforma.x1
            if jogador.y == y and  valor1 < jogador.x and  valor2 > jogador.x: 
                pode_cair = False 
                jogador.no_chao = True

        draw_polygonon(tela, plataforma.vertices, "white")

    if pode_cair: aplicar_gravidade(jogador)
    
    dt = clock.tick(60) / 1000

    pygame.display.flip()

pygame.quit()
sys.exit()