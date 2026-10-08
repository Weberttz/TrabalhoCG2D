import pygame

VERMELHO = (148, 13, 19)
VERDE = (22, 117, 33)
BRANCO = (227, 225, 225)

botoes = [
    {"nome": "Reiniciar", "acao": "reiniciar", "x0": 431, "y0": 480, "x1": 831, "y1": 540},
    {"nome": "Menu", "acao": "menu", "x0": 431, "y0": 540, "x1": 831, "y1": 600},
]
opcao_selecionada = 0

def desenhar_tela_final(superficie, estado_jogo, jogador, fonte, fonte_titulo):
    tela_transparente = pygame.Surface((superficie.get_width(), superficie.get_height()), pygame.SRCALPHA)
    tela_transparente.fill((0, 0, 0, 120))
    superficie.blit(tela_transparente, (0, 0))

    cor_titulo = VERDE if estado_jogo == "Win" else VERMELHO
    texto_conteudo = "VICTORY" if estado_jogo == "Win" else "GAME OVER"
    texto_titulo = fonte_titulo.render(texto_conteudo, True, cor_titulo)
    superficie.blit(texto_titulo, (superficie.get_width() // 2 - texto_titulo.get_width() // 2, 100))

    tempo_min = int(jogador.tempo) // 60
    seg = int(jogador.tempo) % 60
    estatisticas = [
        f"Total coletados: {jogador.quantidade_coletada}",
        f"Duração da partida: {tempo_min}min e {seg}s",
        f"Pontuação final: {jogador.pontuacao}"
    ]

    y_estatistica = 200
    for e in estatisticas:
        texto = fonte.render(e, True, BRANCO)
        superficie.blit(texto, (superficie.get_width() // 2 - texto.get_width() // 2, y_estatistica))
        y_estatistica += 30


    for o, opcao in enumerate(botoes):
        if o == opcao_selecionada:
            cor = cor_titulo
            texto = "> " + opcao["nome"]

        else:
            cor = BRANCO
            texto = opcao["nome"]

        superficie_texto = fonte.render(texto, True, cor)
        largura_opcao = opcao["x1"] - opcao["x0"]
        altura_opcao = opcao["y1"] - opcao["y0"]

        x_opcao = opcao["x0"] + largura_opcao // 2 - superficie_texto.get_width() // 2
        y_opcao = opcao["y0"] + altura_opcao // 2 - superficie_texto.get_height() // 2
        superficie.blit(superficie_texto, (x_opcao, y_opcao))


def acao_tela_final(evento):
    global opcao_selecionada

    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_DOWN:
            opcao_selecionada = 1

        elif evento.key == pygame.K_UP:
            opcao_selecionada = 0
        elif evento.key == pygame.K_RETURN:
            opcao = botoes[opcao_selecionada]
            return opcao["acao"]
    
    return None        
