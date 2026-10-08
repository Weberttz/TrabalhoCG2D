import Classes.vetor as v
from Classes.retangulo import Retangulo as r
import Biblioteca.algoritmos as bibgraf
from Biblioteca import transformacoes
from settings import *

uvs = [
    (0, 1),  # inferior-esquerdo
    (0, 0),  # superior-esquerdo
    (1, 0),  # superior-direito
    (1, 1),  # inferior-direito
]

uvs_jogador = [
    (0, 1.0),   # inferior-esquerdo (mantém na base)
    (0, 0.222), # superior-esquerdo (traz o topo para baixo)
    (1, 0), # superior-direito
    (1, 1.0),   # inferior-direito (mantém na base)
]

uvs_coletaveis = [
    (0, 0),  # inferior-esquerdo
    (1, 0),  # superior-esquerdo
    (1, 1),  # superior-direito
    (0, 1) # inferior-direito
]

def desenhar_portal_estilizado(surface, plataforma, camera):
    x_centro = plataforma.x0 + plataforma.largura // 2
    y_centro = plataforma.y1 - plataforma.altura

    rx_base = plataforma.largura // 2
    ry_base = plataforma.altura // 2

    # Atualiza o tempo interno do portal para mover os efeitos
    plataforma.tempo_portal += 0.07

    # Efeito de pulsação
    pulsacao = math.sin(plataforma.tempo_portal * 2) * (rx_base * 0.08)
    rx = rx_base + pulsacao
    ry = ry_base + pulsacao

    centro_tela = camera.aplicar_posicao((x_centro, y_centro))
    cx_tela, cy_tela = int(centro_tela[0]), int(centro_tela[1])

    bibgraf.desenhar_elipse(surface, cx_tela, cy_tela, int(rx * 0.8), int(ry * 0.8), plataforma.cor_borda, preenchida=True)
    bibgraf.desenhar_elipse(surface, cx_tela, cy_tela, int(rx * 0.5), int(ry * 0.5), plataforma.cor, preenchida=True)

def desenhar_portais(jogo):
    for portal in jogo.portais_visiveis:
        desenhar_portal_estilizado(jogo.tela, portal, jogo.camera)

def obter_cor_jogador(jogo):
    cor_efeito = None

    if jogo.jogador.tomando_dano:

        fase = jogo.jogador.tempo_dano // jogo.jogador.tempo_piscar

        if fase % 2 == 0:
            cor_efeito = WHITE
        else:
            cor_efeito = BLACK

        jogo.jogador.tempo_dano -= 1

        if jogo.jogador.tempo_dano <= 0:
            jogo.jogador.tomando_dano = False

    return cor_efeito

def obter_cor_inimigo(inimigo):
    cor_efeito = None

    if inimigo.tomando_dano:

        fase = inimigo.tempo_dano // inimigo.tempo_piscar

        if fase % 2 == 0:
            cor_efeito = VERMELHO
        else:
            cor_efeito = BLACK

        inimigo.tempo_dano -= 1

        if inimigo.tempo_dano <= 0:
            inimigo.tomando_dano = False

    return cor_efeito


def desenhar_jogador(jogo):
    jogador = jogo.jogador
    vertices = jogo.camera.aplicar_vertices(jogo.jogador.vertices)
    imagem = jogo.imagens_jogador.get(jogador.image)
    if imagem != None:
        cor_efeito = obter_cor_jogador(jogo)
        bibgraf.scanline_texture(jogo.tela, vertices, uvs_jogador, imagem, cor_efeito)
    else:
        bibgraf.draw_polygonon(jogo.tela, vertices, BLACK)
        bibgraf.scanline_fill(jogo.tela, vertices, jogo.jogador.cor)

    if jogo.debug:
        vertices_rect = jogo.camera.aplicar_vertices(jogo.jogador.retangulo.vertices)
        aabb = r.calcular_aabb(vertices_rect)
        bibgraf.desenhar_aabb(jogo.tela, aabb, WHITE)

def desenhar_debug_entidades(jogo, vertices, entidade):
    texto = jogo.fonte.render(f"Vida: {entidade.vida}", 1, WHITE)
    jogo.tela.blit(texto, (vertices[1][0], vertices[1][1] - 20))
    vertices_rect = jogo.camera.aplicar_vertices(entidade.retangulo.vertices)
    aabb = r.calcular_aabb(vertices_rect)
    bibgraf.desenhar_aabb(jogo.tela, aabb, WHITE)

def desenhar_chefe(jogo):
    if jogo.chefe == None: return
    vertices = jogo.camera.aplicar_vertices(jogo.chefe.vertices)
    imagem = jogo.imagens_chefe.get(jogo.chefe.image)
    if imagem is not None:
        cor_efeito = obter_cor_inimigo(jogo.chefe)
        bibgraf.scanline_texture(jogo.tela, vertices, uvs_jogador, imagem, cor_efeito)
    else:
        bibgraf.draw_polygonon(jogo.tela, vertices, BLACK)
        bibgraf.scanline_fill(jogo.tela, vertices, jogo.chefe.cor)

    if jogo.debug:
        desenhar_debug_entidades(jogo, vertices, jogo.chefe)
        return

    texto = jogo.fonte.render(f"Vida: {jogo.chefe.vida}", 1, WHITE)
    jogo.tela.blit(texto, (vertices[1][0], vertices[1][1] - 20))
    

def desenhar_coletaveis(jogo):
    for coletavel in jogo.coletaveis_visiveis:
        vertices = jogo.camera.aplicar_vertices(coletavel.vertices)

        if coletavel.imagem != None:
            bibgraf.scanline_texture(jogo.tela, vertices, uvs_coletaveis, coletavel.imagem)
            if jogo.debug:
                bibgraf.draw_polygonon(jogo.tela, vertices, "red")

def desenhar_aabb_de_portal(jogo):
    for portal in jogo.portais_visiveis:
        vertices = jogo.camera.aplicar_vertices(portal.retangulo.vertices)
        bibgraf.draw_polygonon(jogo.tela, vertices, "red")

def desenhar_projeteis(jogo):
    scroll = -v.Vetor(jogo.camera.retangulo.topleft)
    for projetil in jogo.jogador.equipamento.projeteis:
        projetil.desenhar(jogo.tela, scroll, jogo.camera)

    for pombo in jogo.pombos:
        for pedra in pombo.pedras:
            pedra.desenhar(jogo.tela, scroll, jogo.camera)

    if jogo.chefe != None:
        for livro in jogo.chefe.livros:
            livro.desenhar(jogo.tela, scroll, jogo.camera)


def desenhar_pombos(jogo):
    for pombo in jogo.pombos_visiveis:
        vertices = jogo.camera.aplicar_vertices(pombo.vertices)
        imagem = jogo.imagens_pombos.get(pombo.image)
        if imagem is not None:
            cor_efeito = obter_cor_inimigo(pombo)
            bibgraf.scanline_texture(jogo.tela, vertices, uvs, imagem, cor_efeito)
        else:
            bibgraf.scanline_fill(jogo.tela, vertices, pombo.cor)
            bibgraf.draw_polygonon(jogo.tela, vertices, "red")

        if jogo.debug:
            desenhar_debug_entidades(jogo, vertices, pombo)

def desenhar_zumbis(jogo):
    for zumbi in jogo.zumbis_visiveis:
        vertices = jogo.camera.aplicar_vertices(zumbi.vertices)
        imagem = jogo.imagens_zumbi.get(zumbi.image)
        if imagem is not None:
            cor_efeito = obter_cor_inimigo(zumbi)
            bibgraf.scanline_texture(jogo.tela, vertices, uvs, imagem, cor_efeito)
        else:
            bibgraf.scanline_fill(jogo.tela, vertices, zumbi.cor)
            bibgraf.draw_polygonon(jogo.tela, vertices, "red")

        if jogo.debug:
            desenhar_debug_entidades(jogo, vertices, zumbi)

def desenhar_cachorros(jogo):
    for cachorro in jogo.cachorros_visiveis:
        vertices = jogo.camera.aplicar_vertices(cachorro.vertices)
        imagem = jogo.imagens_cachorro.get(cachorro.image)

        if imagem is not None:
            bibgraf.scanline_texture(jogo.tela, vertices, uvs, imagem)
        else:
            bibgraf.scanline_fill(jogo.tela, vertices, cachorro.cor)
            bibgraf.draw_polygonon(jogo.tela, vertices, "red")

        if jogo.debug:
            desenhar_debug_entidades(jogo, vertices, cachorro)

def corte_borda_viewport(vertices_view, viewport):
    Vxmin, Vymin, Vxmax, Vymax = viewport
    x0 = vertices_view[0][0]
    y0 = vertices_view[0][1]
    x1 = vertices_view[2][0]
    y1 = vertices_view[2][1]
    
    if (x1 > Vxmax or x0 < Vxmin 
        or y0 < Vymin or y1 > Vymax):
        _, rx0, ry0, rx1, ry1 = bibgraf.cohen_sutherland( x0, y0, x1, y1, Vxmin, Vymin, Vxmax, Vymax)
        x0, y0, x1, y1 = rx0, ry0, rx1, ry1
    
    vertices_view[0][0], vertices_view[1][0] = x0, x0
    vertices_view[0][1], vertices_view[3][1] = y0, y0
    vertices_view[2][0], vertices_view[3][0] = x1, x1
    vertices_view[1][1], vertices_view[2][1] = y1, y1
    return vertices_view


def desenhar_viewport(jogo, matriz_viewport, viewport):
    
    Vxmin, Vymin, Vxmax, Vymax = viewport

    borda = [
        (Vxmin, Vymin),
        (Vxmax, Vymin),
        (Vxmax, Vymax),
        (Vxmin, Vymax)
    ]

    jogo.tela.blit(jogo.viewport_surface, borda[0])

    limites_camera = jogo.camera.retangulo
    j = jogo.jogador

    jogador_view = [transformacoes.produto_matriz(matriz_viewport,
                    [[vertice[0]+ limites_camera.left],[vertice[1]+ limites_camera.top],[1]])
                     for vertice in j.retangulo.vertices]

    jogador_view = corte_borda_viewport(jogador_view,viewport)
         
    bibgraf.scanline_fill(jogo.tela, jogador_view, j.cor)

    gerenciador = jogo.gerenciadorFases
    if gerenciador.fase_atual == gerenciador.max_fases - 1:
        c = jogo.chefe
        chefe_view = [transformacoes.produto_matriz(matriz_viewport,
                            [[vertice[0]+ limites_camera.left],[vertice[1]+ limites_camera.top],[1]])
                            for vertice in c.retangulo.vertices]
        
        chefe_view = corte_borda_viewport(chefe_view, viewport)
                
        bibgraf.scanline_fill(jogo.tela, chefe_view, c.cor)

    plataformas = [p for p in jogo.plataformas 
                if p.x0 <= LARGURA - limites_camera.left
                and p.x1 >= - limites_camera.left
                and p.y0 <= ALTURA - limites_camera.top
                and p.y1 >= - limites_camera.top]

    
    for plataforma in plataformas:
        plataforma_view =[transformacoes.produto_matriz(matriz_viewport,
                    [[vertice[0] + limites_camera.left],[vertice[1] + limites_camera.top],[1]])
                    for vertice in plataforma.vertices]
        
        # Se tiver intersceção com a borda usa o clipping
        plataforma_view = corte_borda_viewport(plataforma_view,viewport)
        
        bibgraf.scanline_fill(jogo.tela, plataforma_view, plataforma.cor)

    for zumbi in jogo.zumbis_visiveis:
        zumbi_view =[transformacoes.produto_matriz(matriz_viewport,
                            [[vertice[0] + limites_camera.left],[vertice[1] + limites_camera.top],[1]])
                            for vertice in zumbi.vertices]
        
        zumbi_view = corte_borda_viewport(zumbi_view, viewport)

        bibgraf.scanline_fill(jogo.tela, zumbi_view, VERDE)

    for cachorro in jogo.cachorros_visiveis:
        cachorro_view =[transformacoes.produto_matriz(matriz_viewport,
                                    [[vertice[0] + limites_camera.left],[vertice[1] + limites_camera.top],[1]])
                                    for vertice in cachorro.vertices]
        x0 = cachorro_view[0][0]
        y0 = cachorro_view[0][1]
        x1 = cachorro_view[2][0]
        y1 = cachorro_view[1][1]
        
        if (x1 > Vxmax or x0 < Vxmin 
            or y0 < Vymin or y1 > Vymax):
            _, rx0, ry0, rx1, ry1 = bibgraf.cohen_sutherland( x0, y0, x1, y1, Vxmin, Vymin, Vxmax, Vymax)
            x0, y0, x1, y1 = rx0, ry0, rx1, ry1

        cachorro_view[0][0], cachorro_view[1][0] = x0, x0
        cachorro_view[0][1], cachorro_view[3][1] = y0, y0
        cachorro_view[2][0], cachorro_view[3][0] = x1, x1
        cachorro_view[1][1], cachorro_view[2][1] = y1, y1

        bibgraf.scanline_fill(jogo.tela, cachorro_view, cachorro.cor)

    for pombo in jogo.pombos_visiveis:
        pombo_view =[transformacoes.produto_matriz(matriz_viewport,
                                    [[vertice[0] + limites_camera.left],[vertice[1] + limites_camera.top],[1]])
                                    for vertice in pombo.vertices]
        x0 = pombo_view[0][0]
        y0 = pombo_view[0][1]
        x1 = pombo_view[2][0]
        y1 = pombo_view[1][1]
        
        if (x1 > Vxmax or x0 < Vxmin 
            or y0 < Vymin or y1 > Vymax):
            _, rx0, ry0, rx1, ry1 = bibgraf.cohen_sutherland( x0, y0, x1, y1, Vxmin, Vymin, Vxmax, Vymax)
            x0, y0, x1, y1 = rx0, ry0, rx1, ry1

        pombo_view[0][0], pombo_view[1][0] = x0, x0
        pombo_view[0][1], pombo_view[3][1] = y0, y0
        pombo_view[2][0], pombo_view[3][0] = x1, x1
        pombo_view[1][1], pombo_view[2][1] = y1, y1

        bibgraf.scanline_fill(jogo.tela, pombo_view, pombo.cor)


    bibgraf.draw_polygonon(jogo.tela, borda, WHITE)

    return

def desenhar_hud(jogo):
    if jogo.jogador.vida >= 70:
        cor = VERDE
    elif jogo.jogador.vida >= 40:
        cor = AMARELO 
    else:
        cor = VERMELHO

    fonte_vida = pygame.font.SysFont("Arial", 20, bold=True)
    cheia = fonte_vida.render("█" * int(jogo.jogador.vida / 5), True, cor)
    vazia = fonte_vida.render("░" * int((VIDA_MAXIMA - jogo.jogador.vida) / 5), True, (100, 100, 100))
    texto_municao = jogo.fonte.render(f"Munição: {jogo.jogador.equipamento.municao}", 1, AMARELO)
    texto_pontuacao = jogo.fonte.render(f"Pontuação: {jogo.jogador.pontuacao}", 1, AMARELO)
    texto_coletaveis = jogo.fonte.render(f"Coletáveis: {jogo.jogador.quantidade_coletada}", 1, AMARELO)

    jogo.tela.blit(cheia, (30, 10))
    jogo.tela.blit(vazia, (30 + cheia.get_width(), 10))
    jogo.tela.blit(texto_municao, (30, 40))
    jogo.tela.blit(texto_coletaveis, (30, 70))
    jogo.tela.blit(texto_pontuacao, (30, 100))

    janela_mundo = (0, 0, LARGURA, ALTURA + 10)

    M_minimapa = transformacoes.matriz_janela_viewport(janela_mundo, jogo.viewport)

    desenhar_viewport(jogo, M_minimapa, jogo.viewport)

