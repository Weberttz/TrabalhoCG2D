import sys
from Gerenciador import Renderizador 
from Gerenciador import Atualizador

from settings import *
from Biblioteca.algoritmos import *
from Classes.jogador import Jogador
from Classes.camera import Camera
from Classes.arma import Arma
from Auxiliar.inicializacao import *

from menu import iniciar_menu, desenhar_menu, acao_menu

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Jogo")
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Myriad Pro", 30)

        self.rodando = True
        self.debug = False
        self.fases = ["./Mapas/fase1.csv", "./Mapas/fase2.csv","./Mapas/fase3.csv"]
        self.larguras = [len(carregar_mapa(self.fases[0])[0]) * TAMANHO_QUADRADO, 
                         len(carregar_mapa(self.fases[1])[0]) * TAMANHO_QUADRADO, 
                         len(carregar_mapa(self.fases[2])[0]) * TAMANHO_QUADRADO ]
        
        self.fase_atual = 0
        self.max_fases = 3
        self.run_finalizada = False
        self.voltando = False

        self.tempo_animacao = 0.0
        self.avancar_frame = False
        self.zumbis_visiveis = []
        self.coletaveis_visiveis = []

        self.estado_jogo = "menu"
        iniciar_menu()

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

        if self.fase_atual == 0 and self.voltando == False:
            arma = Arma(60, POS_INICIO.copy(), "yellow")
            self.jogador = Jogador(POS_INICIO.copy(), self.plataformas, self.zumbis, 
                                self.coletaveis, [arma], "red")
        else:
            self.jogador.plataformas = self.plataformas
            self.jogador.coletaveis = self.coletaveis
            self.jogador.inimigos = self.zumbis

        self.camera = Camera(self.jogador, self.largura_mapa, self.altura_mapa)

        for z in self.zumbis:
            z.image = self.anim_idle[0]
            z.inimigos.append(self.jogador)

        self.mundo_surface = self.renderizar_mundo()
        self.voltando = False

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
            dt = self.clock.tick(60) / 1000 # único tick por frame
            self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar()

        pygame.quit()
        sys.exit()

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

            #pega a acao de determinado botao do menu e atualiza o estado do jogo
            if self.estado_jogo == "menu":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    acao = acao_menu(pygame.mouse.get_pos())
                    if acao == "jogar":
                        self.estado_jogo = "jogando"
                    elif acao == "sair":
                        self.rodando = False

            if self.estado_jogo == "jogando":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_h:
                        self.debug = not self.debug
                

    # Atualização
    def atualizar(self, dt):
        Atualizador.atualizar_jogador(self)
        self.camera.atualizar()

        self.zumbis[:] = [z for z in self.zumbis if z.vivo]   # in-place: mantém a lista compartilhada
        Atualizador.atualizar_animacao(self, dt)
        Atualizador.atualizar_entidades(self, dt)

    # Renderização
    def desenhar(self):
        #comeca desenhando o menu q é o estado inicial do jogo
        if self.estado_jogo == "menu":
            desenhar_menu(self.tela, (pygame.mouse.get_pos()))

        #comeca o jogo apenas se o estado foi alterado para "jogando" a partir do retorno de acao_menu
        elif self.estado_jogo == "jogando":
            self.tela.fill(AZUL_NOTURNO)
            self.tela.blit(self.mundo_surface, self.camera.retangulo.topleft)

            Renderizador.desenhar_jogador(self)
            Renderizador.desenhar_coletaveis(self)
            Renderizador.desenhar_projeteis(self)
            Renderizador.desenhar_zumbis(self)
            Renderizador.desenhar_hud(self)

        pygame.display.flip()

if __name__ == "__main__":
    Jogo().rodar()