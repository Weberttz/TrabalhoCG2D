import pygame
import sys

from Biblioteca.algoritmos import (
    linha_bresenham,
    scanline_fill,
    flood_fill_iterativo,
    desenhar_circulo,
    draw_polygonon,
    retangulo_para_poligono,
    desenhar_elipse,
    bresenham_circulo,
    scanline_fill_gradiente,
    scanline_texture,
)

COR_CEU = (31, 34, 59)
AZUL_ESCURO = (46, 51, 87)
BEGE = (115, 115, 112)
CINZA = (122, 122, 122)
CINZA_ESCURO = (74, 74, 74)
BRANCO = (227, 225, 225)
COR_LUA = (238, 220, 130)
COR_ELIPSE = (255, 255, 255, 80)
COR_TRONCO_ARVORE = (66, 60, 41)
COR_FOLHAS = (68, 99, 67)
COR_ENTRADA = (43, 45, 54)
COR_JANELA = (166, 161, 113)
VERDE_ESCURO = (18, 87, 36)
AZUL_RU = (3, 6, 69)
COR_JANELA_RU = (18, 18, 18)
COR_JANELA_RU2 = (46, 45, 45)
PRETO = (26, 26, 26)
COR_TELHADO_BLOCO = (69, 13, 8)
COR_GRADES = (8, 48, 15)
AZUL_CLARO = (25, 54, 105)
VERMELHO = (112, 15, 15)
CAMINHO_FONTE = "Assets/PressStart2P-Regular.ttf"

superficie_nuvem = None
superficie_lua = None
superficie_arbusto = None
superficie_arvore = None
superficie_nupeinsc = None
superficie_predio_r = None
superficie_predio_generico1 = None
superficie_predio_generico2 = None
superficie_predio_generico3 = None
superficie_arvore_maior = None
superficie_arbusto_maior = None
superficie_calcada = None
superficie_rua = None
superficie_ru = None
superficie_nupeinsc = None
superficie_carrinho = None
superficie_blocoG = None
superficie_biblioteca = None

cenarios_fases = {}
predios_cenario_atual = []
vegetacao_cenario_atual = []

textura_tijolos = pygame.image.load("Assets/textura-tijolos.jpg")
textura_tapioca = pygame.image.load("Assets/tapioca.png")

def desenhar_NC2A():
    largura, altura = 360, 300
    superficie_nc2a = pygame.Surface((largura, altura), pygame.SRCALPHA)

    vertices_parede = retangulo_para_poligono(0, 0, largura, altura)
    scanline_fill(superficie_nc2a, vertices_parede, BEGE)

    vertices_retangulo_topo = retangulo_para_poligono(0, - 15, largura, 15)
    scanline_fill(superficie_nc2a, vertices_retangulo_topo, AZUL_ESCURO)

    vertices_retangulo_meio = retangulo_para_poligono(0, 135, largura, 15)
    scanline_fill(superficie_nc2a, vertices_retangulo_meio, AZUL_ESCURO)

    colunas_x = [
        20,
        120,
        220,
        320,
    ]

    for cx in colunas_x:
        vertices_coluna = retangulo_para_poligono(cx, 15, 20, 285)
        scanline_fill(superficie_nc2a, vertices_coluna, AZUL_ESCURO)

    vertices_entrada = retangulo_para_poligono(145, 250, 70, 50)
    scanline_fill(superficie_nc2a, vertices_entrada, COR_ENTRADA)

    x_colunas = [40, 140, 240]
    y_linhas = [45, 175]

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

def desenhar_predio_generico2():
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

def desenhar_ru():
    largura_parede, altura_parede = 650, 250
    largura_topo, altura_topo = 700, 120
    altura_total = altura_parede + altura_topo
    largura_janela, altura_janela = 80, 110
    largura_porta, altura_porta = 150, 200

    largura_superficie_janela = 5 * largura_janela
    altura_superficie_janela = 2 * altura_janela 

    x_parede = (largura_topo - largura_parede) // 2

    superficie_ru = pygame.Surface((largura_topo, altura_total), pygame.SRCALPHA)
    superficie_janelas = pygame.Surface((largura_superficie_janela, altura_superficie_janela))

    uvs = [
        (0,0),
        (1,0),
        (1,1),
        (0,1)
    ]

    vertices_ru = retangulo_para_poligono(x_parede, altura_topo, largura_parede, altura_parede)
    scanline_texture(superficie_ru, vertices_ru, uvs, textura_tijolos)

    cores_janelas = [
        COR_JANELA_RU, COR_JANELA_RU, COR_JANELA_RU2, COR_JANELA_RU2
    ]

    for linha in range(2):
        for coluna in range(5):
            x = coluna * largura_janela
            y = linha * altura_janela

            vertices_janelas = retangulo_para_poligono(x, y, largura_janela, altura_janela)
            scanline_fill_gradiente(superficie_janelas, vertices_janelas, cores_janelas)
            draw_polygonon(superficie_janelas, vertices_janelas, BRANCO)

    vertices_porta = retangulo_para_poligono(x_parede + 450, altura_topo + 50, largura_porta, altura_porta)
    scanline_fill_gradiente(superficie_ru, vertices_porta, cores_janelas)
    draw_polygonon(superficie_ru, vertices_porta, BRANCO)

    x_janela = x_parede
    y_janela = altura_topo
    superficie_ru.blit(superficie_janelas, (x_janela, y_janela))
    vertices_topo = retangulo_para_poligono(0, 1, largura_topo, altura_topo)
    scanline_fill(superficie_ru, vertices_topo, AZUL_RU)

    return superficie_ru

def desenhar_nupeinsc():
    largura, altura = 420, 300
    superficie_nupeinsc = pygame.Surface((largura, altura), pygame.SRCALPHA)

    vertices_parede = retangulo_para_poligono(0, 0, largura, altura)
    scanline_fill(superficie_nupeinsc, vertices_parede, COR_JANELA)

    vertices_retangulo_topo = retangulo_para_poligono(0, 0, largura, 20)
    scanline_fill(superficie_nupeinsc, vertices_retangulo_topo, BRANCO)

    vertices_retangulo_meio = retangulo_para_poligono(0, 85, largura, 10)
    scanline_fill(superficie_nupeinsc, vertices_retangulo_meio, BRANCO)

    vertices_retangulo_meio2 = retangulo_para_poligono(0, 170, largura, 10)
    scanline_fill(superficie_nupeinsc, vertices_retangulo_meio2, BRANCO)

    vertices_retangulo_meio2 = retangulo_para_poligono(0, 245, largura, 5)
    scanline_fill(superficie_nupeinsc, vertices_retangulo_meio2, BRANCO)
    
    colunas_x = [
        0,
        81,
        162,
        243,
        324,
        405,
    ]

    for cx in colunas_x:
        vertices_coluna = retangulo_para_poligono(cx, 15, 15, 285)
        scanline_fill(superficie_nupeinsc, vertices_coluna, BRANCO)

    vertices_entrada = retangulo_para_poligono(177, 250, 65, 60)
    scanline_fill(superficie_nupeinsc, vertices_entrada, COR_JANELA_RU)

    x_colunas = [15, 96, 177, 258, 339]
    y_linhas = [15, 95, 180]


    cores_janelas = [
        COR_JANELA_RU, COR_JANELA_RU, COR_JANELA_RU2, COR_JANELA_RU2
    ]

    for y_janela in y_linhas:
        for x_janela in x_colunas:
            janela = retangulo_para_poligono(x_janela, y_janela, 65, 55)
            scanline_fill_gradiente(superficie_nupeinsc, janela, cores_janelas)
            x_centro = x_janela + 32
            linha_bresenham(superficie_nupeinsc, x_centro, y_janela, x_centro, y_janela + 55, BRANCO)
    return superficie_nupeinsc


def desenhar_carrinho_billy():
    largura_base, altura_base  = 150, 80
    largura_teto, altura_teto = 160, 20
    largura_pilar, altura_pilar = 8, 50
    largura_total = largura_teto
    raio_roda = 8
    altura_total = altura_teto + altura_pilar + altura_base + raio_roda + 2

    superficie_carrinho = pygame.Surface((largura_total, altura_total), pygame.SRCALPHA)

    x_base = (largura_teto - largura_base) // 2
    y_base = altura_teto + altura_pilar
    vertices_base = retangulo_para_poligono(x_base, y_base, largura_base, altura_base)
    scanline_fill(superficie_carrinho, vertices_base, AZUL_CLARO)
    uvs = [
        (0,0),
        (1,0),
        (1,1),
        (0,1)
    ]
    
    scanline_texture(superficie_carrinho, vertices_base, uvs, textura_tapioca)
    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 10)
    
    texto_tapioca = fonte_titulo.render("tapioca billy", True, BRANCO)
    superficie_carrinho.blit(texto_tapioca, (x_base + 10, y_base + 50))

    vertices_teto = retangulo_para_poligono(0, 0, largura_teto, altura_teto)
    scanline_fill(superficie_carrinho, vertices_teto, BRANCO)

    vertices_pilar1 = retangulo_para_poligono(x_base + 15, altura_teto, largura_pilar, altura_pilar)
    scanline_fill(superficie_carrinho, vertices_pilar1, BRANCO)
    
    vertices_pilar2 = retangulo_para_poligono(x_base + largura_base - 25, altura_teto, largura_pilar, altura_pilar)
    scanline_fill(superficie_carrinho, vertices_pilar2, BRANCO)

    yc = altura_base + y_base
    xc1 = x_base + 30
    xc2 = x_base + largura_base - 30

    bresenham_circulo(superficie_carrinho, xc1, yc, raio_roda, PRETO)
    flood_fill_iterativo(superficie_carrinho, xc1, yc, PRETO, PRETO)

    bresenham_circulo(superficie_carrinho, xc2, yc, raio_roda, PRETO)
    flood_fill_iterativo(superficie_carrinho, xc2, yc, PRETO, PRETO)

    return superficie_carrinho

def desenhar_blocoG():
    largura_bloco, altura_bloco = 800, 320
    largura_telhado, altura_telhado = 830, 20
    altura_total = altura_bloco + altura_telhado
    largura_total = largura_telhado + 500
    largura_faixa = largura_bloco 
    altura_faixa = 30
#105 - meio, altura grade 20
    largura_grade, altura_grade = 8, 40
    largura_topo_grade, altura_topo_grade = largura_bloco, 5

    x_bloco = 15
    superficie_blocoG = pygame.Surface((largura_total, altura_total), pygame.SRCALPHA)

    vertices_bloco = retangulo_para_poligono(x_bloco, altura_telhado, largura_bloco, altura_bloco)
    scanline_fill(superficie_blocoG, vertices_bloco, BRANCO)

    vertices_telhado = retangulo_para_poligono(0, 0, largura_telhado, altura_telhado)
    scanline_fill(superficie_blocoG, vertices_telhado, COR_TELHADO_BLOCO)

    vertices_faixa1 = retangulo_para_poligono(x_bloco, altura_telhado, largura_faixa, altura_faixa)
    scanline_fill(superficie_blocoG, vertices_faixa1, BEGE)

    COR_SOMBRA = (80, 80, 80)
    vertices_sombra1 = retangulo_para_poligono(x_bloco, altura_telhado + altura_faixa - 2, largura_bloco, 8)
    scanline_fill(superficie_blocoG, vertices_sombra1, COR_SOMBRA)

    vertices_faixa2 = retangulo_para_poligono(x_bloco, altura_telhado + 150, largura_faixa, altura_faixa)
    scanline_fill(superficie_blocoG, vertices_faixa2, BEGE)

    vertices_sombra2 = retangulo_para_poligono(x_bloco, altura_telhado + 150 + altura_faixa - 2, largura_bloco, 8)
    scanline_fill(superficie_blocoG, vertices_sombra2, COR_SOMBRA)

    cores_portas = [
        COR_JANELA_RU, COR_JANELA_RU, COR_JANELA_RU2, COR_JANELA_RU2
    ]

    largura_porta, altura_porta = 50, 80
    num_portas = 5
    y_porta_baixo = altura_telhado + altura_bloco - altura_porta
    y_porta_cima = altura_telhado + 150 - altura_porta
    distancia = largura_bloco // num_portas
    for i in range(num_portas):
        x_centro = x_bloco + (i * distancia) + (distancia // 2)
        x_porta = x_centro - (largura_porta // 2)
    
        vertices_porta = retangulo_para_poligono(x_porta, y_porta_baixo, largura_porta, altura_porta)
        scanline_fill_gradiente(superficie_blocoG, vertices_porta, cores_portas)

    for i in range(num_portas):
        x_centro = x_bloco + (i * distancia) + (distancia // 2)
        x_porta = x_centro - (largura_porta // 2)
        
        vertices_porta = retangulo_para_poligono(x_porta, y_porta_cima, largura_porta, altura_porta)
        scanline_fill_gradiente(superficie_blocoG, vertices_porta, cores_portas)

    x_fim = largura_bloco + 15 - largura_grade
    x_colunas_grade = list(range(x_bloco, x_fim + 1, 70))

    for cx in x_colunas_grade:
        vertices_colunas_grade = retangulo_para_poligono(cx, altura_telhado + 110, largura_grade, altura_grade)
        scanline_fill(superficie_blocoG, vertices_colunas_grade, COR_GRADES)

    vertices_topo_grade = retangulo_para_poligono(x_bloco, altura_telhado + 110, largura_topo_grade, altura_topo_grade)
    scanline_fill(superficie_blocoG, vertices_topo_grade, COR_GRADES)


    largura_g, altura_g = 160, 160
    vertices_g = retangulo_para_poligono(largura_telhado + 20, altura_telhado + altura_bloco - altura_g, largura_g, altura_g)
    scanline_fill(superficie_blocoG, vertices_g, BRANCO)    
    largura_g_menor, altura_g_menor = 80, 80
    vertices_g_menor = retangulo_para_poligono(largura_telhado + 60, altura_telhado + altura_bloco - 1.5 * altura_g_menor  , largura_g_menor, altura_g_menor)
    scanline_fill(superficie_blocoG, vertices_g_menor, AZUL_ESCURO)
    
    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 35)

    texto_G = fonte_titulo.render("G", True, BRANCO)
    superficie_blocoG.blit(texto_G, (largura_telhado + 85, altura_telhado + altura_bloco -  altura_g_menor -16 ))


    return superficie_blocoG

def desenhar_rua():
    largura_calcada, altura_calcada = 1262, 50
    largura_rua, altura_rua = 1262, 120
    altura_total = 170
    superficie_rua = pygame.Surface((largura_rua, altura_total), pygame.SRCALPHA)
    vertices_calcada = retangulo_para_poligono(0, 0, largura_calcada, altura_calcada)
    vertices_rua = retangulo_para_poligono(0, 50, largura_rua, altura_rua)
    scanline_fill(superficie_rua, vertices_calcada, CINZA_ESCURO)
    scanline_fill(superficie_rua, vertices_rua, VERDE_ESCURO)

    return superficie_rua

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
    global superficie_lua, superficie_nuvem, superficie_arbusto, superficie_nupeinsc, superficie_arvore, superficie_predio_r, superficie_predio_generico1, superficie_predio_generico2, superficie_predio_generico3, cenarios_fases, superficie_arbusto_maior, superficie_arvore_maior, superficie_rua, predios_cenario_atual, vegetacao_cenario_atual, superficie_ru, superficie_nupeinsc, superficie_carrinho, superficie_blocoG

    superficie_lua = desenhar_lua(50)
    superficie_arvore = desenhar_arvore()
    superficie_nupeinsc = desenhar_NC2A()
    superficie_arbusto = desenhar_arbusto()
    superficie_nuvem = desenhar_nuvem()
    superficie_predio_r = desenhar_predio_r()
    superficie_predio_generico1 = desenhar_predio_generico1()
    superficie_predio_generico2 = desenhar_predio_generico2()
    superficie_predio_generico3 = desenhar_predio_generico3()
    superficie_arvore_maior = pygame.transform.scale(superficie_arvore, (200, 350))
    superficie_arbusto_maior = pygame.transform.scale(superficie_arbusto, (150, 130))
    superficie_rua = desenhar_rua()
    superficie_ru = desenhar_ru()
    superficie_nupeinsc = desenhar_nupeinsc()
    superficie_carrinho = desenhar_carrinho_billy()
    superficie_blocoG = desenhar_blocoG()

    cenarios_fases = {
        #largura das fases: [5632, 6464, 6304]
        #largura nc2a: 360
        #largura reitoria 500
        #largura prediog1 250
        #largura prediog2 300
        #largura predio g3 200
        #largura arbusto 120
        0 : {
            "predios" : [
                # (100, superficie_ru),
                # (100, superficie_nupeinsc),
                (300, superficie_carrinho),
                # (250, superficie_blocoG),
                # (1100, superficie_predio_generico1),
                (1700, superficie_carrinho),
                (2300, superficie_predio_generico3),
            ],
            "vegetacao" : [
                (100, superficie_arvore),
                (200, superficie_arbusto),
                (900, superficie_arbusto),
                (1400, superficie_arvore_maior),
                (1500, superficie_arbusto_maior),
                (2500, superficie_arvore_maior),
            ]
        },

        1 : {
            "predios" : [
                (500, superficie_predio_r),
                (1100, superficie_predio_generico1),
                (1700, superficie_predio_generico2),
                (2300, superficie_predio_generico3),
            ],

            "vegetacao" : [
                (100, superficie_arvore_maior),
                (200, superficie_arbusto),
                (900, superficie_arbusto),
                (1400, superficie_arvore_maior),
                (1500, superficie_arbusto_maior),
                (2500, superficie_arvore_maior),
            ]
        }

        # 2 : {
        #     "predios" : [
       #         ()
        #     ]
        # }
    }

def carregar_estruturas_fase(indice_fase):
    global predios_cenario_atual, vegetacao_cenario_atual
    informacao = cenarios_fases.get(indice_fase, {})
    predios_cenario_atual = informacao.get("predios", [])
    vegetacao_cenario_atual = informacao.get("vegetacao", []) 
    


def desenhar_cenario(superficie, x_camera, y_chao=690, largura_tela=1262):

    superficie.fill(COR_CEU)

    if superficie_lua:
        superficie.blit(superficie_lua, (200, 50))
    
    if superficie_nuvem:
        superficie.blit(superficie_nuvem, ((350, 40)))
        superficie.blit(superficie_nuvem, ((650, 50)))

    if superficie_rua:
        superficie.blit(superficie_rua, (0, 550))

    for x_mundo, superficie_predio in predios_cenario_atual:
        x_tela = x_mundo - int(x_camera * 0.3)
        largura_predio = superficie_predio.get_width()

        if -largura_predio <= x_tela <= largura_tela:
            posicao_y = y_chao - superficie_predio.get_height()
            superficie.blit(superficie_predio, (x_tela, posicao_y - 120))


    for x_mundo, superficie_vegetacao in vegetacao_cenario_atual:
        x_tela = x_mundo - int(x_camera * 0.6)
        largura = superficie_vegetacao.get_width()

        if -largura <= x_tela <= largura_tela:
            posicao_y = y_chao - superficie_vegetacao.get_height()
            superficie.blit(superficie_vegetacao, (x_tela, posicao_y - 40))


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
