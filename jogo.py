import sys
import pygame

from settings import *
from BibliotecaGrafica.algoritmos import *
from Classes.jogador import Jogador
from Classes.camera import Camera
from Classes.arma import Arma
from Auxiliar.inicializacao import *

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Jogo")
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Myriad Pro", 30)

        self.rodando = True
        self.debug = False
        self.fases = ["./Mapas/fase5.csv", "./Mapas/fase3.csv","./Mapas/fase4.csv"]
        self.fase_atual = 0
        self.max_fases = 3
        self.run_finalizada = False

        self.tempo_animacao = 0.0
        self.avancar_frame = False
        self.zumbis_visiveis = []
        self.coletaveis_visiveis = []

        self.carregar_sprites()
        self.carregar_fase(self.fases[self.fase_atual])

    # Inicialização
    def carregar_sprites(self):
        self.anim_idle = gerar_lista_animacoes("zumbi", "idle", 8)
        self.anim_esquerda = gerar_lista_animacoes("zumbi", "walk_left", 8)
        self.anim_direita = gerar_lista_animacoes("zumbi", "walk_right", 8)

        imagens = {}
        for lista in (self.anim_idle, self.anim_esquerda, self.anim_direita):
            imagens |= carregar_animacoes(lista)

        # redimensiona uma vez só, na carga -> matrizes de escala
        self.imagens_zumbi = {nome: pygame.transform.scale(img, (30, 30))
                              for nome, img in imagens.items()}

    def carregar_fase(self, caminho):
        mapa = carregar_mapa(caminho)
        self.plataformas, self.blocks, self.coletaveis = criar_level(mapa)
        self.zumbis = criar_zumbis(self.plataformas, self.blocks)

        self.largura_mapa = len(mapa[0]) * TAMANHO_QUADRADO
        self.altura_mapa = len(mapa) * TAMANHO_QUADRADO

        arma = Arma(60, POS_INICIO.copy(), "yellow")
        self.jogador = Jogador(POS_INICIO.copy(), self.plataformas, self.zumbis, 
                               self.coletaveis, [arma], "red")
        self.camera = Camera(self.jogador, self.largura_mapa, self.altura_mapa)

        for z in self.zumbis:
            z.image = self.anim_idle[0]
            z.inimigos.append(self.jogador)

        self.mundo_surface = self.renderizar_mundo()

    def renderizar_mundo(self):
        """Desenha o mapa estático uma única vez numa superficie gigante."""
        surface = pygame.Surface((self.largura_mapa, self.altura_mapa), pygame.SRCALPHA)
        for plataforma in self.plataformas:
            draw_polygonon(surface, plataforma.vertices, BLACK)
            scanline_fill(surface, plataforma.vertices, plataforma.cor)
        return surface

    # Loop principal
    def rodar(self):
        while self.rodando:
            dt = self.clock.tick(60) / 1000   # único tick por frame
            self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar()

        pygame.quit()
        sys.exit()

    def tratar_eventos(self):
        keys = pygame.key.get_pressed()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            if keys[pygame.K_h]:
                self.debug = not self.debug

    # Atualização
    def atualizar(self, dt):
        self.verificar_morte_jogador()
        self.verificar_passou_de_fase()
        self.jogador.atualizar()
        self.camera.atualizar()

        self.zumbis[:] = [z for z in self.zumbis if z.vivo]   # in-place: mantém a lista compartilhada
        self.atualizar_visiveis()
        self.atualizar_coletaveis()
        self.atualizar_projeteis(dt)
        self.atualizar_animacao(dt)
        self.atualizar_zumbis()

    def verificar_morte_jogador(self):
        j = self.jogador
        if j.vida <= 0 or j.pos.y > self.altura_mapa:
            j.pos = POS_INICIO.copy()
            j.vida = 100

    def verificar_passou_de_fase(self):
        j = self.jogador
        if j.pos.x > self.largura_mapa:
            j.pos = POS_INICIO.copy()
            self.fase_atual+=1

            if self.fase_atual == self.max_fases:
                self.fase_atual -= 1
                self.run_finalizada = True
                return

            self.carregar_fase(self.fases[self.fase_atual])

    def atualizar_visiveis(self):
        dx, _ = self.camera.camera.topleft
        self.zumbis_visiveis = [
            z for z in self.zumbis
            if -dx - z.tamanho <= z.pos.x <= -dx + LARGURA
        ]
        self.coletaveis_visiveis = [
            c for c in self.coletaveis
            if -dx - c.tamanho <= c.pos.x <= -dx + LARGURA
        ]

    def atualizar_coletaveis(self):
        coletaveis = self.coletaveis
        coletaveis[:] = [c for c in coletaveis if c.ativo]

    def atualizar_projeteis(self, dt):
        projeteis = self.jogador.equipamento.projetils
        projeteis[:] = [p for p in projeteis if p.ativo]   # remove os que não estão ativos
        for projetil in projeteis:
            projetil.atualizar(dt)

    def atualizar_animacao(self, dt):
        self.tempo_animacao += dt
        self.avancar_frame = self.tempo_animacao >= VEL_ANIMACAO
        if self.avancar_frame:
            self.tempo_animacao = 0.0

    def atualizar_zumbis(self):
        projeteis = self.jogador.equipamento.projetils
        for zumbi in self.zumbis_visiveis:
            zumbi.atualizar(projeteis)
            if self.avancar_frame:
                zumbi.animar(self.anim_idle, self.anim_esquerda, self.anim_direita)

    # Renderização
    def desenhar(self):
        self.tela.fill(AZUL_NOTURNO)
        self.tela.blit(self.mundo_surface, self.camera.camera.topleft)

        self.desenhar_jogador()
        self.desenhar_coletaveis()
        self.desenhar_projeteis()
        self.desenhar_zumbis()
        self.desenhar_hud()

        pygame.display.flip()

    def desenhar_jogador(self):
        vertices = self.camera.aplicar_vertices(self.jogador.vertices)
        draw_polygonon(self.tela, vertices, BLACK)
        scanline_fill(self.tela, vertices, self.jogador.cor)

    def desenhar_coletaveis(self):
        for coletavel in self.coletaveis_visiveis:
            if coletavel.tipo == "moeda":
                vertices = self.camera.aplicar_vertices(coletavel.retangulo.vertices)
                scanline_fill(self.tela, vertices, coletavel.cor)
                draw_polygonon(self.tela, vertices, "red")
            else:
                desenhar_circulo(self.tela, coletavel.centro, coletavel.raio, coletavel.cor, True)

    def desenhar_projeteis(self):
        scroll = -Vetor(self.camera.camera.topleft)
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
                scanline_fill(self.tela, vertices, zumbi.cor)
                draw_polygonon(self.tela, vertices, "red")

            if self.debug:
                texto = self.fonte.render(f"Vida: {zumbi.vida}", 1, WHITE)
                self.tela.blit(texto, (vertices[1][0], vertices[1][1] - 20))
                dx, dy = self.camera.camera.topleft
                zumbi.retangulo.move_ip(dx, dy)
                aabb = Retangulo.calcular_aabb(zumbi.retangulo.vertices)
                desenhar_aabb(self.tela, aabb, "white")

    def desenhar_hud(self):
        texto_vida = self.fonte.render(f"Vida: {self.jogador.vida}", 1, WHITE)
        texto_municao = self.fonte.render(f"Munição: {self.jogador.equipamento.municao}", 1, WHITE)
        texto_coletaveis = self.fonte.render(f"Coletáveis: {self.jogador.quantidade_coletada}", 1, WHITE)

        self.tela.blit(texto_vida, (30, 10))
        self.tela.blit(texto_municao, (30, 40))
        self.tela.blit(texto_coletaveis, (30, 70))
                
if __name__ == "__main__":
    Jogo().rodar()