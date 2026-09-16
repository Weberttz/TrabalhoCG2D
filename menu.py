import pygame
import sys

from BibliotecaGrafica.algoritmos import set_pixel, linha_bresenham, flood_fill_iterativo, bresenham_circulo

LARGURA, ALTURA = 1262, 722
CAMINHO_FONTE = "TrabalhoCG2D/Assets/PressStart2P-Regular.ttf"
CAMINHO_FUNDO = "TrabalhoCG2D/Assets/uece_noite.png"
COR_BOTAO = pygame.Color('#538645')
COR_HOVER =  pygame.Color("#729D65") #VERDE + CLARO
COR_BORDA_BOTAO = pygame.Color("#335F27") #VERDE + ESCURO
COR_TEXTO = pygame.Color("#D1F4C7")
COR_TITULO = pygame.Color("#508640")

fonte = None
fonte_titulo = None
imagem_fundo = None
superficie_circulo = None

botoes = [
    {"nome": "JOGAR", "acao": "jogar", "x0": 431, "y0": 250, "x1": 831, "y1": 330},
    {"nome": "INSTRUÇÕES", "acao": "instrucoes", "x0": 431, "y0": 360, "x1": 831, "y1": 440},
    {"nome": "SAIR", "acao": "sair", "x0": 431, "y0": 470, "x1": 831, "y1": 550}
]

def criar_superficie_botao(largura, altura, cor, cor_borda):
    superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
    linha_bresenham(superficie, 0, 0, largura - 1, 0, cor_borda)
    linha_bresenham(superficie, 0, 0, 0, altura - 1, cor_borda)

#   efeito de profundidade nas bordas de baixo e da direita
    profundidade = 8
    for i in range(profundidade):
        linha_bresenham(superficie, largura - 1 - i, i, largura -1 - i, altura - 1 - i, cor_borda)
        linha_bresenham(superficie, i, altura - 1 - i, largura - 1 - i, altura - 1 - i, cor_borda)

    x_centro = largura // 2
    y_centro = altura // 2
    flood_fill_iterativo(superficie, x_centro, y_centro, cor, cor_borda)

    return superficie

def criar_superficie_circulo(raio, cor):
    diametro = raio * 2 + 1
    superficie = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
    centro = raio

    bresenham_circulo(superficie, centro, centro, raio, cor)
    flood_fill_iterativo(superficie, centro, centro, cor, cor)

    return superficie


def iniciar_menu():
    global fonte, fonte_titulo, imagem_fundo, superficie_circulo

    fonte = pygame.font.Font(CAMINHO_FONTE, 18)
    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 38)

    imagem_fundo = pygame.image.load(CAMINHO_FUNDO)

    #pre renderiza o circulo/lua
    superficie_circulo = criar_superficie_circulo(50, (238, 238, 224))

    #pre renderiza cada botao no estado normal e no estado de hover
    for botao in botoes:
        largura_botao = botao["x1"] - botao["x0"]
        altura_botao = botao["y1"] - botao["y0"]

        botao["superficie"] = criar_superficie_botao(largura_botao, altura_botao, COR_BOTAO, COR_BORDA_BOTAO)
        botao["superficie_hover"] = criar_superficie_botao(largura_botao, altura_botao, COR_HOVER, COR_BORDA_BOTAO)

def ponto_no_botao(x_ponto, y_ponto, x0, y0, x1, y1):
    return x0 <= x_ponto <= x1 and y0 <= y_ponto <= y1


def desenhar_menu(superficie, posicao_mouse):
    superficie.blit(imagem_fundo, (0, 0))

    texto_titulo = fonte_titulo.render("ZUMBI GAME", True, COR_TITULO)

    titulo_x = LARGURA // 2 - texto_titulo.get_width() // 2

    superficie.blit(texto_titulo, (titulo_x, 100))

    for botao in botoes:
        if ponto_no_botao(posicao_mouse[0], posicao_mouse[1], botao["x0"], botao["y0"], botao["x1"], botao["y1"]):
            superficie_botao = botao["superficie_hover"]
        else:
            superficie_botao = botao["superficie"]

        superficie.blit(superficie_botao, (botao["x0"], botao["y0"]))

        texto = fonte.render(botao["nome"], True, COR_TEXTO)

        largura_botao = botao["x1"] - botao["x0"]
        altura_botao = botao["y1"] - botao["y0"]

        x_texto = botao["x0"] + largura_botao // 2 - texto.get_width() // 2
        y_texto = botao["y0"] + altura_botao // 2 - texto.get_height() // 2

        superficie.blit(texto, (x_texto, y_texto))

    superficie.blit(superficie_circulo, (1060 - 52, 80 - 52))

#identifica o clique do mouse e retorna o nome da acao associada ao botao
def clique_menu(posicao_mouse):
    x_mouse, y_mouse = posicao_mouse

    for botao in botoes:
        if ponto_no_botao(x_mouse, y_mouse, botao["x0"], botao["y0"], botao["x1"], botao["y1"]):
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
                acao = clique_menu(posicao_mouse)

                if acao == "sair":
                    rodando = False

        desenhar_menu(tela, posicao_mouse)
        pygame.display.flip()

    pygame.quit()
    sys.exit()