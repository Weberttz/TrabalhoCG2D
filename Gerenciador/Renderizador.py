import Classes.vetor as v
import Classes.retangulo as r
import Biblioteca.algoritmos as bibgraf
from settings import WHITE

def desenhar_jogador(self):
    vertices = self.camera.aplicar_vertices(self.jogador.vertices)
    bibgraf.draw_polygonon(self.tela, vertices, BLACK)
    bibgraf.scanline_fill(self.tela, vertices, self.jogador.cor)

def desenhar_coletaveis(self):
    for coletavel in self.coletaveis_visiveis:
        if coletavel.tipo == "moeda":
            vertices = self.camera.aplicar_vertices(coletavel.retangulo.vertices)
            bibgraf.scanline_fill(self.tela, vertices, coletavel.cor)
            bibgraf.draw_polygonon(self.tela, vertices, "red")
        else:
            bibgraf.desenhar_circulo(self.tela, coletavel.centro, coletavel.raio, coletavel.cor, True)

def desenhar_projeteis(self):
    scroll = -v.Vetor(self.camera.camera.topleft)
    for projetil in self.jogador.equipamento.projetils:
        projetil.desenhar(self.tela, scroll, self.camera)

def desenhar_zumbis(self):
    for zumbi in self.zumbis_visiveis:
        vertices = self.camera.aplicar_vertices(zumbi.vertices)
        imagem = self.imagens_zumbi.get(zumbi.image)

        if imagem is not None:
            pos_tela = vertices[1]   # canto superior-esquerdo já com câmera
            self.tela.blit(imagem, pos_tela)
        else:
            bibgraf.scanline_fill(self.tela, vertices, zumbi.cor)
            bibgraf.draw_polygonon(self.tela, vertices, "red")

        if self.debug:
            texto = self.fonte.render(f"Vida: {zumbi.vida}", 1, WHITE)
            self.tela.blit(texto, (vertices[1][0], vertices[1][1] - 20))
            dx, dy = self.camera.camera.topleft
            zumbi.retangulo.move_ip(dx, dy)
            aabb = r.Retangulo.calcular_aabb(zumbi.retangulo.vertices)
            r.desenhar_aabb(self.tela, aabb, "white")

def desenhar_hud(self):
    texto_vida = self.fonte.render(f"Vida: {self.jogador.vida}", 1, WHITE)
    texto_municao = self.fonte.render(f"Munição: {self.jogador.equipamento.municao}", 1, WHITE)
    texto_coletaveis = self.fonte.render(f"Coletáveis: {self.jogador.quantidade_coletada}", 1, WHITE)

    self.tela.blit(texto_vida, (30, 10))
    self.tela.blit(texto_municao, (30, 40))
    self.tela.blit(texto_coletaveis, (30, 70))
                
