import Classes.vetor as v
from Classes.retangulo import Retangulo as r
import Biblioteca.algoritmos as bibgraf
from Biblioteca import transformacoes
from settings import WHITE, BLACK, LARGURA, ALTURA

def desenhar_jogador(jogo):
    vertices = jogo.camera.aplicar_vertices(jogo.jogador.vertices)
    bibgraf.draw_polygonon(jogo.tela, vertices, BLACK)
    bibgraf.scanline_fill(jogo.tela, vertices, jogo.jogador.cor)

    if jogo.debug:
        vertices_rect = jogo.camera.aplicar_vertices(jogo.jogador.retangulo.vertices)
        aabb = r.calcular_aabb(vertices_rect)
        bibgraf.desenhar_aabb(jogo.tela, aabb, WHITE)

def desenhar_coletaveis(jogo):
    for coletavel in jogo.coletaveis_visiveis:
        if coletavel.tipo == "moeda":
            vertices = jogo.camera.aplicar_vertices(coletavel.retangulo.vertices)
            bibgraf.scanline_fill(jogo.tela, vertices, coletavel.cor)
            bibgraf.draw_polygonon(jogo.tela, vertices, "red")
        else:
            vertices = jogo.camera.aplicar_vertices(coletavel.retangulo.vertices)
            bibgraf.scanline_fill(jogo.tela, vertices, coletavel.cor)
            bibgraf.draw_polygonon(jogo.tela, vertices, "red")
            # bibgraf.desenhar_circulo(jogo.tela, coletavel.centro, coletavel.raio, coletavel.cor, True)

def desenhar_projeteis(jogo):
    scroll = -v.Vetor(jogo.camera.retangulo.topleft)
    for projetil in jogo.jogador.equipamento.projetils:
        projetil.desenhar(jogo.tela, scroll, jogo.camera)

def desenhar_zumbis(jogo):
    for zumbi in jogo.zumbis_visiveis:
        vertices = jogo.camera.aplicar_vertices(zumbi.vertices)
        imagem = jogo.imagens_zumbi.get(zumbi.image)

        if imagem is not None:
            pos_tela = vertices[1]   # canto superior-esquerdo já com câmera
            jogo.tela.blit(imagem, pos_tela)
        else:
            bibgraf.scanline_fill(jogo.tela, vertices, zumbi.cor)
            bibgraf.draw_polygonon(jogo.tela, vertices, "red")

        if jogo.debug:
            texto = jogo.fonte.render(f"Vida: {zumbi.vida}", 1, WHITE)
            jogo.tela.blit(texto, (vertices[1][0], vertices[1][1] - 20))
            vertices_rect = jogo.camera.aplicar_vertices(zumbi.retangulo.vertices)
            aabb = r.calcular_aabb(vertices_rect)
            bibgraf.desenhar_aabb(jogo.tela, aabb, WHITE)

def desenhar_viewport(jogo, matriz_viewport, viewport):

    Vxmin, Vymin, Vxmax, Vymax = viewport

    borda = [
        (Vxmin, Vymin),
        (Vxmax, Vymin),
        (Vxmax, Vymax),
        (Vxmin, Vymax)
    ]

    j = jogo.jogador

    jogador_view = transformacoes.aplica_transformacao(matriz_viewport, j.retangulo.vertices)

    bibgraf.scanline_fill(jogo.tela , jogador_view, j.cor)

    plataformas = [p for p in jogo.plataformas if p.x1 < LARGURA and p.y0 < ALTURA]

    for plataforma in plataformas:
        plataforma_view = transformacoes.aplica_transformacao(matriz_viewport, plataforma.vertices)
        bibgraf.scanline_fill(jogo.tela, plataforma_view, plataforma.cor)

    bibgraf.draw_polygonon(jogo.tela, borda, WHITE)

    return

def desenhar_hud(jogo):
    texto_vida = jogo.fonte.render(f"Vida: {jogo.jogador.vida}", 1, WHITE)
    texto_municao = jogo.fonte.render(f"Munição: {jogo.jogador.equipamento.municao}", 1, WHITE)
    texto_coletaveis = jogo.fonte.render(f"Coletáveis: {jogo.jogador.quantidade_coletada}", 1, WHITE)

    jogo.tela.blit(texto_vida, (30, 10))
    jogo.tela.blit(texto_municao, (30, 40))
    jogo.tela.blit(texto_coletaveis, (30, 70))
    viewport_minimapa = (1000, 10, 1250, 200)
    janela_mundo = (0, 0, LARGURA, ALTURA + 10)
    M_minimapa = bibgraf.janela_viewport(janela_mundo, viewport_minimapa)
    desenhar_viewport(jogo, M_minimapa,  viewport_minimapa)

