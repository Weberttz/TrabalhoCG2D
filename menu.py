import pygame
import sys

from Biblioteca.algoritmos import linha_bresenham, flood_fill_iterativo, bresenham_circulo, desenhar_elipse

LARGURA, ALTURA = 1262, 722
CAMINHO_FONTE = "./Assets/PressStart2P-Regular.ttf"
CAMINHO_FUNDO = "./Assets/uece-noite.png"
COR_BOTAO = pygame.Color('#538645')
COR_HOVER =  pygame.Color("#729D65") #VERDE + CLARO
COR_BORDA_BOTAO = pygame.Color("#335F27") #VERDE + ESCURO
COR_TEXTO = pygame.Color("#D1F4C7")
COR_TITULO = pygame.Color("#508640")
COR_LUA = (238, 220, 130)
COR_NUVEM = (255, 255, 255, 80) #Com parametro alpha de transparencia

fonte = None
fonte_titulo = None
imagem_fundo = None
superficie_circulo = None
superficie_elipse = None
superficie_nuvem = None

botoes = [
    {"nome": "JOGAR", "acao": "jogar", "x0": 431, "y0": 250, "x1": 831, "y1": 330},
    {"nome": "INSTRUÇÕES", "acao": "instrucoes", "x0": 431, "y0": 360, "x1": 831, "y1": 440},
    {"nome": "SAIR", "acao": "sair", "x0": 431, "y0": 470, "x1": 831, "y1": 550}
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
    '''Inicializa o menu, criando as superfícies pré-renderizadas.'''
    global fonte, fonte_titulo, imagem_fundo, superficie_circulo, superficie_nuvem

    fonte = pygame.font.Font(CAMINHO_FONTE, 18)
    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 38)

    imagem_fundo = pygame.image.load(CAMINHO_FUNDO)

    #pre renderiza o circulo/lua
    superficie_circulo = criar_superficie_circulo(50, COR_LUA)
    superficie_nuvem = criar_superficie_nuvem(COR_NUVEM, COR_NUVEM)
    #pre renderiza cada botao no estado normal e no estado de hover
    for botao in botoes:
        largura_botao = botao["x1"] - botao["x0"]
        altura_botao = botao["y1"] - botao["y0"]

        botao["superficie"] = criar_superficie_botao(largura_botao, altura_botao, COR_BOTAO, COR_BORDA_BOTAO)
        botao["superficie_hover"] = criar_superficie_botao(largura_botao, altura_botao, COR_HOVER, COR_BORDA_BOTAO)

def ponto_no_botao(ponto_x, ponto_y, x0, y0, x1, y1):
    return x0 <= ponto_x <= x1 and y0 <= ponto_y <= y1

def desenhar_menu(superficie, posicao_mouse):
    '''Desenha menu pré-renderizado na tela.'''
    superficie.blit(imagem_fundo, (0, 0))

    texto_titulo = fonte_titulo.render("ZUMBI GAME", True, COR_TITULO)

    titulo_x = LARGURA // 2 - texto_titulo.get_width() // 2

    superficie.blit(texto_titulo, (titulo_x, 100))
    superficie.blit(superficie_nuvem, (80, 40))

    for botao in botoes:
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


def acao_menu(posicao_mouse):
    '''Identifica o clique do mouse e retorna o 
        nome da ação associada ao botão.'''
    mouse_x, mouse_y = posicao_mouse

    for botao in botoes:
        if ponto_no_botao(mouse_x, mouse_y, botao["x0"], botao["y0"], botao["x1"], botao["y1"]):
            return botao["acao"]

    return None


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


