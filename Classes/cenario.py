import pygame
import os
import sys
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Biblioteca.algoritmos import (
    linha_bresenham,
    scanline_fill,
    flood_fill_iterativo,
    desenhar_circulo,
    draw_polygonon,
    retangulo_para_poligono,
    desenhar_elipse,
    bresenham_circulo,
)

COR_CEU = (31, 34, 59)
AZUL_ESCURO = (46, 51, 87)
BEGE = (115, 115, 112)
CINZA = (122, 122, 122)
BRANCO = (227, 225, 225)
COR_LUA = (238, 220, 130)
COR_ELIPSE = (255, 255, 255, 80)
COR_TRONCO_ARVORE = (66, 60, 41)
COR_FOLHAS = (68, 99, 67)
COR_ENTRADA = (43, 45, 54)
COR_JANELA = (166, 161, 113)

superficie_nuvem = None
superficie_lua = None
superficie_arbusto = None
superficie_arvore = None
superficie_nc2a = None
superficie_predio_r = None
superficie_predio_generico1 = None
superficie_predio_generico2 = None
superficie_predio_generico3 = None

estruturas_fase = {}

estruturas_fase_atual = []

def desenhar_NC2A():
    largura, altura = 360, 300
    superficie_nc2a = pygame.Surface((largura, altura), pygame.SRCALPHA)

    vertices_parede = retangulo_para_poligono(0, 0, largura, altura)
    scanline_fill(superficie_nc2a, vertices_parede, BEGE)

    vertices_retangulo_topo = retangulo_para_poligono(0, 0 - 15, largura, 15)
    scanline_fill(superficie_nc2a, vertices_retangulo_topo, AZUL_ESCURO)

    vertices_retangulo_meio = retangulo_para_poligono(0, 0 + 135, largura, 15)
    scanline_fill(superficie_nc2a, vertices_retangulo_meio, AZUL_ESCURO)

    colunas_x = [
        0 + 20,
        0 + 120,
        0 + 220,
        0 + 320,
    ]

    for cx in colunas_x:
        vertices_coluna = retangulo_para_poligono(cx, 0 + 15, 20, 285)
        scanline_fill(superficie_nc2a, vertices_coluna, AZUL_ESCURO)

    vertices_entrada = retangulo_para_poligono(0 + 145, 0 + 250, 70, 50)
    scanline_fill(superficie_nc2a, vertices_entrada, COR_ENTRADA)

    x_colunas = [0 + 40, 0 + 140, 0 + 240]
    y_linhas = [0 + 45, 0 + 175]

    for y_janela in y_linhas:
        for x_janela in x_colunas:
            janela = retangulo_para_poligono(x_janela, y_janela, 80, 60)
            scanline_fill(superficie_nc2a, janela, COR_JANELA)
            draw_polygonon(superficie_nc2a, janela, COR_JANELA)

    return superficie_nc2a


def desenhar_predio_generico1():
    largura, altura = 250, 400
    superficie_predio_generico1 = pygame.Surface((largura, altura), pygame.SRCALPHA)

    vertices_predio = retangulo_para_poligono(0, 0, largura, altura)
    scanline_fill(superficie_predio_generico1, vertices_predio, CINZA)

    return superficie_predio_generico1

def desenhar_predio_generido2():
    largura, altura = 300, 300
    superficie_predio_generico2 = pygame.Surface((largura, altura), pygame.SRCALPHA)

    vertices_predio = retangulo_para_poligono(0, 0, largura, altura)
    scanline_fill(superficie_predio_generico2, vertices_predio, BRANCO)
    return superficie_predio_generico2

def desenhar_predio_generico3():
    largura, altura = 200, 350
    superficie_predio_generico3 = pygame.Surface((largura, altura), pygame.SRCALPHA)

    vertices_predio = retangulo_para_poligono(0, 0, largura, altura)
    scanline_fill(superficie_predio_generico3, vertices_predio, BEGE)
    return superficie_predio_generico3

def desenhar_arvore():
    largura, altura = 150, 300
    superficie_arvore = pygame.Surface((largura, altura), pygame.SRCALPHA)
    vertices_tronco = retangulo_para_poligono(55, 120, 40, 160)
    scanline_fill(superficie_arvore, vertices_tronco, COR_TRONCO_ARVORE)

    circulos = [
        ((55, 80), 45),
        ((95, 85), 45),
        ((60, 50), 35),
        ((90, 50), 35),
        ((60, 110), 35),
        ((90, 110), 35),
    ]

    for centro, raio in circulos:
        desenhar_circulo(superficie_arvore, centro, raio, COR_FOLHAS, True)
    return superficie_arvore


def desenhar_arbusto():
    largura, altura = 120, 100
    superficie_arbusto = pygame.Surface((largura, altura), pygame.SRCALPHA)

    circulos = [
        ((60, 45), 35),
        ((35, 50), 25),
        ((85, 50), 25),
        ((60, 30), 25),
    ]

    for centro, raio in circulos:
        desenhar_circulo(superficie_arbusto, centro, raio, COR_FOLHAS, True)
    return superficie_arbusto


def desenhar_nuvem():
    largura, altura = 260, 110
    superficie_nuvem = pygame.Surface((largura, altura), pygame.SRCALPHA)

    elipses = [(50, 30, 10, 25), (60, 40, 65, 5), (50, 30, 145, 25)]

    for raio_x, raio_y, posicao_x, posicao_y in elipses:
        centro_x = posicao_x + raio_x
        centro_y = posicao_y + raio_y
        desenhar_elipse(superficie_nuvem, centro_x, centro_y, raio_x, raio_y, BRANCO)
        flood_fill_iterativo(superficie_nuvem, centro_x, centro_y, BRANCO, BRANCO)

    return superficie_nuvem


def desenhar_lua(raio):
    diametro = raio * 2 + 1
    superficie_lua = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
    centro = raio
    bresenham_circulo(superficie_lua, centro, centro, raio, COR_LUA)
    flood_fill_iterativo(superficie_lua, centro, centro, COR_LUA, COR_LUA)
    return superficie_lua


def desenhar_predio_r():
    largura_paredes_laterais = 150
    altura_paredes_laterais = 250
    largura_parede_central = 200
    altura_parede_central = 260

    largura_pilar = 50
    altura_pilar = 450

    y_chao_superficie = altura_pilar
    y_topo_lateral = y_chao_superficie - altura_paredes_laterais
    y_topo_central = y_chao_superficie - altura_parede_central

    largura_total = largura_paredes_laterais * 2 + largura_parede_central

    superficie_predio_r = pygame.Surface((largura_total, altura_pilar), pygame.SRCALPHA)

    largura_placa = 160
    altura_placa = 65

    parede_esquerda = [
        (0, y_chao_superficie),
        (0 + largura_paredes_laterais, y_chao_superficie),
        (0 + largura_paredes_laterais, y_topo_lateral),
        (0, y_topo_lateral + 50),
    ]
    scanline_fill(superficie_predio_r, parede_esquerda, BRANCO)

    x_central = largura_paredes_laterais
    parede_central = retangulo_para_poligono(
        x_central, y_topo_central, largura_parede_central, altura_parede_central
    )
    scanline_fill(superficie_predio_r, parede_central, BRANCO)
    draw_polygonon(superficie_predio_r, parede_central, (0, 0, 0))

    pilar = retangulo_para_poligono(
        x_central + 5, y_chao_superficie - altura_pilar, largura_pilar, altura_pilar
    )
    scanline_fill(superficie_predio_r, pilar, BRANCO)

    placa = retangulo_para_poligono(
        x_central + 20, y_topo_central + 65, largura_placa, altura_placa
    )
    scanline_fill(superficie_predio_r, placa, AZUL_ESCURO)

    placa2 = retangulo_para_poligono(
        x_central + 20, y_topo_central - 40, largura_placa, altura_placa
    )
    scanline_fill(superficie_predio_r, placa2, BRANCO)
    draw_polygonon(superficie_predio_r, placa2, (0, 0, 0))

    degrau1 = retangulo_para_poligono(x_central + 20, y_chao_superficie - 15, 160, 15)
    scanline_fill(superficie_predio_r, degrau1, CINZA)
    degrau2 = retangulo_para_poligono(x_central + 30, y_chao_superficie - 30, 140, 15)
    scanline_fill(superficie_predio_r, degrau2, CINZA)
    degrau3 = retangulo_para_poligono(x_central + 40, y_chao_superficie - 45, 120, 15)
    scanline_fill(superficie_predio_r, degrau3, CINZA)

    largura_entrada, altura_entrada = 80, 60
    entrada = retangulo_para_poligono(
        x_central + 60, y_chao_superficie - 105, largura_entrada, altura_entrada
    )
    scanline_fill(superficie_predio_r, entrada, COR_ENTRADA)

    largura_janela, altura_janela = 100, 55
    janela1 = retangulo_para_poligono(
        25, y_chao_superficie - 82, largura_janela, altura_janela
    )
    scanline_fill(superficie_predio_r, janela1, AZUL_ESCURO)
    draw_polygonon(superficie_predio_r, janela1, CINZA)

    # linha_vertical_janela1
    linha_bresenham(
        superficie_predio_r,
        75,
        y_chao_superficie - 82 + 55,
        75,
        y_chao_superficie - 82,
        BRANCO,
    )
    # linha_horizontal_janela1
    linha_bresenham(
        superficie_predio_r,
        25,
        y_chao_superficie - 55,
        125,
        y_chao_superficie - 55,
        BRANCO,
    )

    janela2 = retangulo_para_poligono(
        25, y_chao_superficie - 161, largura_janela, altura_janela
    )
    scanline_fill(superficie_predio_r, janela2, AZUL_ESCURO)
    draw_polygonon(superficie_predio_r, janela2, CINZA)

    # linha_vertical_janela2
    linha_bresenham(
        superficie_predio_r,
        75,
        y_chao_superficie - 161 + 55,
        75,
        y_chao_superficie - 161,
        BRANCO,
    )
    # linha_horizontal_janela2
    linha_bresenham(
        superficie_predio_r,
        25,
        y_chao_superficie - 135,
        125,
        y_chao_superficie - 135,
        BRANCO,
    )

    x_parede_direita = x_central + largura_parede_central
    parede_direita = [
        (x_parede_direita, y_chao_superficie),
        (x_parede_direita + largura_paredes_laterais, y_chao_superficie),
        (x_parede_direita + largura_paredes_laterais, y_topo_lateral + 40),
        (x_parede_direita, y_topo_lateral),
    ]
    scanline_fill(superficie_predio_r, parede_direita, BRANCO)

    janela3 = retangulo_para_poligono(
        x_parede_direita + 25, y_chao_superficie - 82, largura_janela, altura_janela
    )
    scanline_fill(superficie_predio_r, janela3, AZUL_ESCURO)
    draw_polygonon(superficie_predio_r, janela3, CINZA)

    # linha_vertical_janela3
    linha_bresenham(
        superficie_predio_r,
        x_parede_direita + 75,
        y_chao_superficie - 82 + 55,
        x_parede_direita + 75,
        y_chao_superficie - 82,
        BRANCO,
    )
    # linha_horizontal_janela3
    linha_bresenham(
        superficie_predio_r,
        x_parede_direita + 25,
        y_chao_superficie - 55,
        x_parede_direita + 125,
        y_chao_superficie - 55,
        BRANCO,
    )

    janela4 = retangulo_para_poligono(
        x_parede_direita + 25, y_chao_superficie - 161, largura_janela, altura_janela
    )
    scanline_fill(superficie_predio_r, janela4, AZUL_ESCURO)
    draw_polygonon(superficie_predio_r, janela4, CINZA)

    # linha_vertical_janela4
    linha_bresenham(
        superficie_predio_r,
        x_parede_direita + 75,
        y_chao_superficie - 161 + 55,
        x_parede_direita + 75,
        y_chao_superficie - 161,
        BRANCO,
    )
    # linha_horizontal_janela4
    linha_bresenham(
        superficie_predio_r,
        x_parede_direita + 25,
        y_chao_superficie - 135,
        x_parede_direita + 125,
        y_chao_superficie - 135,
        BRANCO,
    )

    pontos_sombra1 = [
        (placa2[3][0], placa2[3][1]),
        (placa2[2][0], placa2[2][1]),
        (placa[1][0] - 20, placa[1][1]),
        (placa[0][0] + 20, placa[0][1]),
    ]
    scanline_fill(superficie_predio_r, pontos_sombra1, CINZA)

    pontos_sombra2 = [
        (placa[3][0], placa[3][1]),
        (placa[2][0], placa[2][1]),
        (entrada[1][0] - 8, entrada[1][1]),
        (entrada[0][0] + 8, entrada[0][1]),
    ]
    scanline_fill(superficie_predio_r, pontos_sombra2, CINZA)

    return superficie_predio_r


def iniciar_cenario():
    global superficie_lua, superficie_nuvem, superficie_arbusto, superficie_nc2a, superficie_arvore, superficie_predio_r, superficie_predio_generico1, superficie_predio_generico2, superficie_predio_generico3, estruturas_fase

    superficie_lua = desenhar_lua(50)
    superficie_arvore = desenhar_arvore()
    superficie_nc2a = desenhar_NC2A()
    superficie_arbusto = desenhar_arbusto()
    superficie_nuvem = desenhar_nuvem()
    superficie_predio_r = desenhar_predio_r()
    superficie_predio_generico1 = desenhar_predio_generico1()
    superficie_predio_generico2 = desenhar_predio_generido2()
    superficie_predio_generico3 = desenhar_predio_generico3()

    estruturas_fase = {
        #largura das fases: [5632, 6464, 6304]
        #largura nc2a: 360
        #largura reitoria 500
        #largura prediog1 250
        #largura prediog2 300
        #largura predio g3 200
        0 : [
            (100, superficie_predio_generico1),
            (450, superficie_arvore),
            (550, superficie_arbusto),
            (1000, superficie_nc2a),
            (1500, superficie_predio_generico2),
            (2000, superficie_arvore),
            (2100, superficie_arbusto),
            (2200, superficie_predio_generico3),
        ],

        # 1: [

        # ], 

        # 2: [

        # ]
    }

def carregar_estruturas_fase(indice_fase):
    global estruturas_fase_atual
    estruturas_fase_atual = estruturas_fase.get(indice_fase, [])


def desenhar_cenario(superficie, x_camera, y_chao=690, largura_tela=1262):

    superficie.fill(COR_CEU)
    parallax_predios = 0.3

    for x_mundo, superficie_estrutura in estruturas_fase_atual:
        x_tela = x_mundo - int(x_camera * parallax_predios)
        largura_predio = superficie_estrutura.get_width()

        if -largura_predio <= x_tela <= largura_tela:
            posicao_y = y_chao - superficie_estrutura.get_height()
            superficie.blit(superficie_estrutura, (x_tela, posicao_y))

    if superficie_lua:
        superficie.blit(superficie_lua, (1000, 50))

    if superficie_nuvem:
        superficie.blit(superficie_nuvem, ((80, 40)))
        superficie.blit(superficie_nuvem, ((400, 50)))

    if superficie_arvore:
        x_arvore = 900 - int(x_camera * 0.6)
        if -140 <= x_arvore <= superficie.get_width():
            superficie.blit(superficie_arvore, (x_arvore, y_chao - 280))

    if superficie_arbusto:
        x_arbusto = 1000 - int(x_camera * 0.6)
        if -120 <= x_arbusto <= superficie.get_width():
            superficie.blit(superficie_arbusto, (x_arbusto, y_chao - 80))


if __name__ == "__main__":
    import sys

    pygame.init()
    relogio = pygame.time.Clock()

    LARGURA, ALTURA = 1262, 722
    tela = pygame.display.set_mode((LARGURA, ALTURA))

    x_camera = 0

    rodando = True

    while rodando:
        relogio.tick(60)

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT]:
            x_camera += 12
        if teclas[pygame.K_LEFT]:
            x_camera -= 12

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        desenhar_cenario(tela, x_camera)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
