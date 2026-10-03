import sys

from Gerenciador import Renderizador 
from Gerenciador import Atualizador
from Gerenciador import Inicializador
from Gerenciador.GerenciadorFases import GerenciadorFases

from settings import *
from Biblioteca.algoritmos import *
from Classes.jogador import Jogador
from Classes.camera import Camera
from Classes.arma import Arma
from Classes.cenario import desenhar_cenario, iniciar_cenario, carregar_estruturas_fase

from menu import iniciar_menu, desenhar_menu, acao_menu

class Jogo:
    def __init__(self):
        pygame.init() 
        pygame.mixer.init()       
        pygame.display.set_caption("Jogo")
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Myriad Pro", 30)
        self.viewport = (1000, 10, 1250, 200)
       
        self.rodando = True
        self.debug = False
        self.gerenciadorFases = GerenciadorFases(["./Mapas/fase1.csv",
             "./Mapas/fase2.csv","./Mapas/fase3.csv"], TAMANHO_QUADRADO)

        iniciar_cenario()
        
        self.run_finalizada = False
        self.voltando = False

        self.tempo_animacao = 0.0
        self.avancar_frame = False
        self.zumbis_visiveis = []
        self.coletaveis_visiveis = []
        self.cachorros_visiseis = []

        self.nivel_dificuldade = None
        self.estado_jogo = "menu"
        iniciar_menu()

        self.carregar_sprites()
        self.carregar_fase(self.gerenciadorFases.caminho_fase_atual())

    # Inicialização
    def carregar_sprites(self):
        self.anim_zumbi_idle = Inicializador.gerar_lista_animacoes("zumbi", "idle", 8)
        self.anim_zumbi_esquerda = Inicializador.gerar_lista_animacoes("zumbi", "walk_left", 8)
        self.anim_zumbi_direita = Inicializador.gerar_lista_animacoes("zumbi", "walk_right", 8)

        imagens = {}
        for lista in (self.anim_zumbi_idle, self.anim_zumbi_esquerda, self.anim_zumbi_direita):
            imagens |= Inicializador.carregar_animacoes(lista)

        # redimensiona uma vez só, na carga -> matrizes de escala
        self.imagens_zumbi = {nome: pygame.transform.scale(img, (32, 32))
                              for nome, img in imagens.items()}

        self.anim_cachorro_idle = Inicializador.gerar_lista_animacoes("dog", "idle", 5)
        self.anim_cachorro_esquerda = Inicializador.gerar_lista_animacoes("dog", "walk_left", 8)
        self.anim_cachorro_direita = Inicializador.gerar_lista_animacoes("dog", "walk_right", 8)

        imagens = {}
        for lista in (self.anim_cachorro_idle, self.anim_cachorro_esquerda, self.anim_cachorro_direita):
            imagens |= Inicializador.carregar_animacoes(lista)

        # redimensiona uma vez só, na carga -> matrizes de escala
        self.imagens_cachorro = {nome: pygame.transform.scale(img, (32, 32))
                                      for nome, img in imagens.items()}
        

    def carregar_fase(self, caminho):
        mapa = Inicializador.carregar_mapa(caminho)
        self.plataformas, self.blocks, self.coletaveis = Inicializador.criar_level(mapa)
        self.zumbis = Inicializador.criar_inimigos("zumbi", self.plataformas, self.blocks, nivel_dificuldade = self.nivel_dificuldade)
        self.cachorros = Inicializador.criar_inimigos("cachorro", self.plataformas, self.blocks, nivel_dificuldade = self.nivel_dificuldade)
        self.pombos = Inicializador.criar_inimigos("pombo", self.plataformas, self.blocks, nivel_dificuldade = self.nivel_dificuldade)
        self.largura_mapa = len(mapa[0]) * TAMANHO_QUADRADO
        self.altura_mapa = len(mapa) * TAMANHO_QUADRADO

        carregar_estruturas_fase(self.gerenciadorFases.fase_atual)

        inimigos = self.zumbis + self.cachorros + self.pombos

        if self.gerenciadorFases.fase_atual == 0 and self.voltando == False:
            arma = Arma(60, POS_INICIO.copy(), "yellow")
            self.jogador = Jogador(POS_INICIO.copy(), self.plataformas, inimigos, 
                                self.coletaveis, [arma], "red")
        else:
            self.jogador.plataformas = self.plataformas
            self.jogador.coletaveis = self.coletaveis
            self.jogador.inimigos = self.zumbis + self.cachorros + self.pombos

        self.camera = Camera(self.jogador, self.largura_mapa, self.altura_mapa)

        for z in self.zumbis:
            z.image = self.anim_zumbi_idle[0]
            z.inimigos.append(self.jogador)

        for c in self.cachorros:
            c.image = self.anim_cachorro_idle[0]
            c.inimigos.append(self.jogador)

        for p in self.pombos:
            p.inimigos.append(self.jogador)

        self.mundo_surface = self.renderizar_mundo()
        self.viewport_surface = self.criar_surface_viewport()
        self.voltando = False 

    def renderizar_mundo(self):
        """Desenha o mapa estático uma única vez numa superficie gigante."""
        surface = pygame.Surface((self.largura_mapa, self.altura_mapa), pygame.SRCALPHA)
        for plataforma in self.plataformas:
            if plataforma.tipo == "normal":
                draw_polygonon(surface, plataforma.vertices, plataforma.cor_borda)
                scanline_fill(surface, plataforma.vertices, plataforma.cor)
            elif plataforma.tipo == "teleport":
                desenhar_elipse(surface, plataforma.x0 + plataforma.largura // 2, plataforma.y1 - plataforma.altura,
                                8, 28, BLACK, preenchida=True)
                desenhar_elipse(surface, plataforma.x0 + plataforma.largura // 2, plataforma.y1 - plataforma.altura,
                                6, 26, plataforma.cor, preenchida=True)
                
        return surface
    
    def criar_surface_viewport(self):
        surface = pygame.Surface((self.viewport[2] - self.viewport[0],
                                 self.viewport[3] - self.viewport[1]))
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                set_pixel(surface, x, y, AZUL_NOTURNO)
        return surface

    # Loop principal
    def rodar(self):
        self.tocar_musica()
        while self.rodando:
            dt = self.clock.tick(60) / 1000 # único tick por frame
            self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar()

        pygame.quit()
        sys.exit()

    def tocar_musica(self):
        pygame.mixer.music.load("Sons/suspense_sobrenatural_loop.wav")
        pygame.mixer.music.set_volume(1.0) # volume: 0 - mudo, 1 - máximo
        pygame.mixer.music.play(-1)

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
        Atualizador.atualizar_animacao(self, dt)
        Atualizador.atualizar_entidades(self, dt)

    # Renderização
    def desenhar(self):
        #comeca desenhando o menu q é o estado inicial do jogo
        if self.estado_jogo == "menu":
            desenhar_menu(self.tela, (pygame.mouse.get_pos()))

        #comeca o jogo apenas se o estado foi alterado para "jogando" a partir do retorno de acao_menu
        elif self.estado_jogo == "jogando":
            x_camera = abs(self.camera.retangulo.x)
            desenhar_cenario(self.tela, x_camera)
            # self.tela.fill(AZUL_NOTURNO)
            self.tela.blit(self.mundo_surface, self.camera.retangulo.topleft)

            Renderizador.desenhar_jogador(self)
            Renderizador.desenhar_coletaveis(self)
            Renderizador.desenhar_projeteis(self)
            Renderizador.desenhar_zumbis(self)
            Renderizador.desenhar_cachorros(self)
            Renderizador.desenhar_pombos(self)
            Renderizador.desenhar_hud(self)
            if self.debug:
                Renderizador.desenhar_aabb_de_portal(self)

        pygame.display.flip()

if __name__ == "__main__":
    Jogo().rodar()