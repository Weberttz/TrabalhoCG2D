import pygame
import sys

from Biblioteca.algoritmos import linha_bresenham, flood_fill_iterativo, bresenham_circulo, desenhar_elipse

LARGURA, ALTURA = 1262, 722
CAMINHO_FONTE = "./Assets/PressStart2P-Regular.ttf"
CAMINHO_FUNDO = "./Assets/uece-noite.png"
COR_BOTAO = pygame.Color("#427133")
COR_HOVER =  pygame.Color("#4E7D41") #VERDE + CLARO
COR_BORDA_BOTAO = pygame.Color("#325828") #VERDE + ESCURO
COR_TEXTO = pygame.Color("#D1F4C7")
COR_TITULO = pygame.Color("#325828")
COR_LUA = (219, 204, 129)
COR_NUVEM = (255, 255, 255, 80) #Com parametro alpha de transparencia
COR_MEDIA = (189, 154, 40)
COR_DIFICIL = (173, 31, 31)
COR_HOVER_MEDIA = (204, 171, 65)
COR_HOVER_DIFICIL = (181, 42, 42)
COR_BORDA_MEDIA = (171, 138, 29)
COR_BORDA_DIFICL =  (150, 20, 20)
COR_VOLTAR = (47, 82, 122)
COR_HOVER_VOLTAR = (54, 90, 133)
COR_BORDA_VOLTAR = (20, 48, 82)

fonte = None
fonte_titulo = None
imagem_fundo = None
superficie_circulo = None
superficie_elipse = None
superficie_nuvem = None

estado_menu = "INICIO"
dificuldade = "FACIL"

botoes_inicio = [
    {"nome": "JOGAR", "acao": "jogar", "x0": 150, "y0": 240, "x1": 550, "y1": 320},
    {"nome": "DIFICULDADE", "acao": "dificuldade", "x0": 150, "y0": 350, "x1": 550, "y1": 430},
    {"nome": "INSTRUÇÕES", "acao": "instrucoes", "x0": 150, "y0": 460, "x1": 550, "y1": 540},
    {"nome": "SAIR", "acao": "sair", "x0": 150, "y0": 570, "x1": 550, "y1": 650},
]

botoes = botoes_inicio

botoes_dificuldade = [
    {"nome": "FACIL", "acao": "facil", "x0": 150, "y0": 250, "x1": 550, "y1": 330, "cor": COR_BOTAO, "hover": COR_HOVER, "borda": COR_BORDA_BOTAO},
    {"nome": "MEDIA", "acao": "media", "x0": 150, "y0": 360, "x1": 550, "y1": 440, "cor": COR_MEDIA, "hover": COR_HOVER_MEDIA, "borda": COR_BORDA_MEDIA},
    {"nome": "DIFICIL", "acao": "dificil", "x0": 150, "y0": 470, "x1": 550, "y1": 550, "cor": COR_DIFICIL, "hover": COR_HOVER_DIFICIL, "borda": COR_BORDA_DIFICL},
    {"nome": "VOLTAR", "acao": "voltar", "x0": 150, "y0": 580, "x1": 550, "y1": 660, "cor": COR_VOLTAR, "hover": COR_HOVER_VOLTAR, "borda": COR_BORDA_VOLTAR},

]

def criar_superficie_botao(largura, altura, cor, cor_borda):
    superficie = pygame.Surface((largura, altura))
    linha_bresenham(superficie, 0, 0, largura - 1, 0, cor_borda)
    linha_bresenham(superficie, 0, 0, 0, altura - 1, cor_borda)

#   efeito de profundidade nas bordas de baixo e da direita usando o bresenham profundidade=8 vezes
    profundidade = 8
    for i in range(profundidade):
        linha_bresenham(superficie, largura - 1 - i, i, largura -1 - i, altura - 1 - i, cor_borda)
        linha_bresenham(superficie, i, altura - 1 - i, largura - 1 - i, altura - 1 - i, cor_borda)

    centro_x = largura // 2
    centro_y = altura // 2
    flood_fill_iterativo(superficie, centro_x, centro_y, cor, cor_borda)

    return superficie

def criar_superficie_circulo(raio, cor):
    diametro = raio * 2 + 1# + 1 p/ ter a msm quantidade de pixels dos dois lados do centro p/ que a borda n fique cortada 
    superficie = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
    centro = raio

    bresenham_circulo(superficie, centro, centro, raio, cor)
    flood_fill_iterativo(superficie, centro, centro, cor, cor)

    return superficie

def criar_superficie_elipse(raio_x, raio_y, cor_borda, cor_preenchimento=None):
    largura = 2 * raio_x + 1 
    altura = 2 * raio_y + 1 
    superficie_elipse = pygame.Surface((largura, altura), pygame.SRCALPHA)

    centro_x = raio_x
    centro_y = raio_y

    desenhar_elipse(superficie_elipse, centro_x, centro_y, raio_x, raio_y, cor_borda)

    if cor_preenchimento:
        flood_fill_iterativo(superficie_elipse, centro_x, centro_y, cor_preenchimento, cor_borda)

    return superficie_elipse

def criar_superficie_nuvem(cor_borda, cor_preenchimento):
    largura, altura = 260, 110
    superficie_nuvem = pygame.Surface((largura, altura), pygame.SRCALPHA)
    #superficie para colocar as 3 elipses que compoem a nuvem

    elipses_nuvem = [ #lista de tuplas com raios e posisoes da elipses
        (50, 30, 10, 25),
        (60, 40, 65, 5),
        (50, 30, 145, 25)
    ]

    for raio_x, raio_y, posicao_x, posicao_y in elipses_nuvem:
        centro_x = posicao_x + raio_x
        centro_y = posicao_y + raio_y
        desenhar_elipse(superficie_nuvem, centro_x, centro_y, raio_x, raio_y, cor_borda)

        flood_fill_iterativo(superficie_nuvem, centro_x, centro_y, cor_preenchimento, cor_borda)


    return superficie_nuvem

def iniciar_menu():
    global fonte, fonte_titulo, imagem_fundo, superficie_circulo, superficie_nuvem

    fonte = pygame.font.Font(CAMINHO_FONTE, 18)
    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 38)

    imagem_fundo = pygame.image.load(CAMINHO_FUNDO)

    #pre renderiza o circulo/lua
    superficie_circulo = criar_superficie_circulo(50, COR_LUA)
    superficie_nuvem = criar_superficie_nuvem(COR_NUVEM, COR_NUVEM)
    
    #pre renderiza cada botao no estado normal e no estado de hover
    for botao in botoes_inicio:
        largura_botao = botao["x1"] - botao["x0"]
        altura_botao = botao["y1"] - botao["y0"]

        botao["superficie"] = criar_superficie_botao(largura_botao, altura_botao, COR_BOTAO, COR_BORDA_BOTAO)
        botao["superficie_hover"] = criar_superficie_botao(largura_botao, altura_botao, COR_HOVER, COR_BORDA_BOTAO)

    for botao in botoes_dificuldade:
        largura_botao = botao["x1"] - botao["x0"]
        altura_botao = botao["y1"] - botao["y0"]

        botao["superficie"] = criar_superficie_botao(largura_botao, altura_botao, botao["cor"], botao["borda"])
        botao["superficie_hover"] = criar_superficie_botao(largura_botao, altura_botao, botao["hover"], botao["borda"])

def ponto_no_botao(ponto_x, ponto_y, x0, y0, x1, y1):
    return x0 <= ponto_x <= x1 and y0 <= ponto_y <= y1


def desenhar_menu(superficie, posicao_mouse):
    global estado_menu
    superficie.blit(imagem_fundo, (0, 0))


    if estado_menu == "INICIO":
        botoes_ativos = botoes_inicio
        texto = "ZUMBI GAME"
    else:
        botoes_ativos = botoes_dificuldade
        texto = "DIFICULDADE"
    # titulo_x = LARGURA // 2 - texto_titulo.get_width() // 4
    titulo_x = 160
    texto_titulo = fonte_titulo.render(texto, True, COR_TITULO)
    print(texto_titulo.get_height())

    superficie.blit(superficie_nuvem, (650, 40))
    superficie.blit(texto_titulo, (titulo_x, 121))

    for botao in botoes_ativos:
        if ponto_no_botao(posicao_mouse[0], posicao_mouse[1], botao["x0"], botao["y0"], botao["x1"], botao["y1"]):
            superficie_botao = botao["superficie_hover"]
        else:
            superficie_botao = botao["superficie"]

        superficie.blit(superficie_botao, (botao["x0"], botao["y0"]))

        texto = fonte.render(botao["nome"], True, COR_TEXTO)

        largura_botao = botao["x1"] - botao["x0"]
        altura_botao = botao["y1"] - botao["y0"]

        texto_x = botao["x0"] + largura_botao // 2 - texto.get_width() // 2
        texto_y = botao["y0"] + altura_botao // 2 - texto.get_height() // 2

        superficie.blit(texto, (texto_x, texto_y))

    superficie.blit(superficie_circulo, (1000, 35))

#identifica o clique do mouse e retorna o nome da acao associada ao botao
def acao_menu(posicao_mouse):
    global estado_menu, dificuldade
    mouse_x, mouse_y = posicao_mouse

    if estado_menu == "INICIO":
        botoes = botoes_inicio
    else:
        botoes = botoes_dificuldade

    for botao in botoes:
        if ponto_no_botao(mouse_x, mouse_y, botao["x0"], botao["y0"], botao["x1"], botao["y1"]):
            acao = botao["acao"]
        
            if acao == "dificuldade":
                estado_menu = "DIFICULDADE"
                return None
            elif acao == "voltar":
                estado_menu = "INICIO"
                return None
            elif acao == "facil":
                dificuldade = "FACIL"
                return None
            elif acao == "media":
                dificuldade = "MEDIA"
                return None
            elif acao == "dificil":
                dificuldade = "DIFICIL"
                return None
            else:
                return acao

    return None

def get_dificuldade():
    return dificuldade

if __name__ == "__main__":
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Menu Jogo")

    iniciar_menu()

    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        relogio.tick(60)
        posicao_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao = acao_menu(posicao_mouse)

                if acao == "sair":
                    rodando = False

        desenhar_menu(tela, posicao_mouse)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


