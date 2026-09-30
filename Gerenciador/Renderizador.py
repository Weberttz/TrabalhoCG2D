import Classes.vetor as v
from Classes.retangulo import Retangulo as r
import Biblioteca.algoritmos as bibgraf
from Biblioteca import transformacoes
from settings import WHITE, BLACK, LARGURA, ALTURA, AZUL_NOTURNO

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
        vertices = jogo.camera.aplicar_vertices(coletavel.retangulo.vertices)
        if coletavel.tipo != "tapioca" and coletavel.tipo != "moeda":
            bibgraf.scanline_fill(jogo.tela, vertices, coletavel.cor)
            bibgraf.draw_polygonon(jogo.tela, vertices, "red")
        else:
            centro_na_tela = jogo.camera.aplicar_posicao(coletavel.centro)
            bibgraf.desenhar_circulo(jogo.tela, centro_na_tela, coletavel.raio, coletavel.cor, True)
            if jogo.debug:
                bibgraf.draw_polygonon(jogo.tela, vertices, "red")


def desenhar_projeteis(jogo):
    scroll = -v.Vetor(jogo.camera.retangulo.topleft)
    for projetil in jogo.jogador.equipamento.projeteis:
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

    jogo.tela.blit(jogo.viewport_surface, borda[0])

    limites_camera = jogo.camera.retangulo
    j = jogo.jogador

    jogador_view = [transformacoes.produto_matriz(matriz_viewport,
                    [[vertice[0]+ limites_camera.left],[vertice[1]+ limites_camera.top],[1]])
                     for vertice in j.retangulo.vertices]
         
    bibgraf.scanline_fill(jogo.tela, jogador_view, j.cor)

    # o jogador tá sendo acompanhado até que ok
    # mas as plataformas acompanham por um tempo e depois somem
    # não por que ainda
    # e seria interessante colocar o clipping aqui para as plataformas
    # que ficam meio dentro, meio fora
    plataformas = [p for p in jogo.plataformas 
                if p.x0 <= LARGURA - limites_camera.left
                and p.x1 >= - limites_camera.left
                and p.y0 <= ALTURA - limites_camera.top
                and p.y1 >= - limites_camera.top]

    for plataforma in plataformas:
        
        plataforma_view =[transformacoes.produto_matriz(matriz_viewport,
            [[vertice[0] + limites_camera.left],[vertice[1] + limites_camera.top],[1]])
            for vertice in plataforma.vertices]
        # remover da view cortar e pegar os novos vertices 
        # depois colocar de volta na view e usar o scanline_fill pra desenhar tudo
        plataforma_blocos_borda = []
        for plataforma in plataforma_view:
            # intersceção com a direita
            if plataforma.x1 > Vxmax:
                plataforma_blocos_borda.append(plataforma)
            elif plataforma.x0 < Vxmin:
                plataforma_blocos_borda.append(plataforma)
            elif plataforma.y0 < Vymin:
                plataforma_blocos_borda.append(plataforma)
            elif plataforma.y1 > Vymax:
                plataforma_blocos_borda.append(plataforma)
        
        
            

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

    janela_mundo = (0, 0, LARGURA, ALTURA + 10)

    M_minimapa = bibgraf.matriz_janela_viewport(janela_mundo, jogo.viewport)

    desenhar_viewport(jogo, M_minimapa, jogo.viewport)

