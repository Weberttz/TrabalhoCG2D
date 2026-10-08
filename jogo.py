import sys, faulthandler

from Gerenciador import Renderizador 
from Gerenciador import Atualizador
from Gerenciador import Inicializador
from Gerenciador.GerenciadorFases import GerenciadorFases

from settings import *
from Biblioteca.algoritmos import *
from Classes.jogador import Jogador
from Classes.camera import Camera
from Classes.arma import Arma
from Classes.cenario import desenhar_cenario, iniciar_cenario
from menu import iniciar_menu, desenhar_menu, acao_menu, get_dificuldade
from tela_final import desenhar_tela_final, acao_tela_final

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
        self.gerenciadorFases = GerenciadorFases(["./Mapas/estagio14.csv",
             "./Mapas/estagio12.csv","./Mapas/estagio13.csv", "./Mapas/estagio14.csv"], TAMANHO_QUADRADO)

        iniciar_cenario()
        
        self.run_finalizada = False
        self.voltando = False

        self.tempo_animacao = 0.0
        self.avancar_frame = False
        self.zumbis_visiveis = []
        self.coletaveis_visiveis = []
        self.cachorros_visiseis = []

        self.estado_jogo = "menu"
        iniciar_menu()

        self.carregar_sprites()
        self.carregar_fase(self.gerenciadorFases.caminho_fase_atual())

        CAMINHO_FONTE = "Assets/PressStart2P-Regular.ttf"
        self.fonte = pygame.font.Font(CAMINHO_FONTE, 20)
        self.fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 60)

    # Inicialização
    def carregar_sprites(self):
        self.anim_zumbi_idle_esquerda = Inicializador.gerar_lista_animacoes("zumbi", "idle_left", 4)
        self.anim_zumbi_idle_direita = Inicializador.gerar_lista_animacoes("zumbi", "idle_right", 4)                
        self.anim_zumbi_esquerda = Inicializador.gerar_lista_animacoes("zumbi", "walk_left", 6)
        self.anim_zumbi_direita = Inicializador.gerar_lista_animacoes("zumbi", "walk_right", 6)

        imagens = {}
        for lista in (self.anim_zumbi_idle_esquerda,
                      self.anim_zumbi_idle_direita, self.anim_zumbi_esquerda, self.anim_zumbi_direita):
            imagens |= Inicializador.carregar_animacoes(lista)

        self.imagens_zumbi = imagens
        self.anim_cachorro_idle = Inicializador.gerar_lista_animacoes("dog", "idle", 5)
        self.anim_cachorro_esquerda = Inicializador.gerar_lista_animacoes("dog", "walk_left", 8)
        self.anim_cachorro_direita = Inicializador.gerar_lista_animacoes("dog", "walk_right", 8)

        imagens = {}
        for lista in (self.anim_cachorro_idle, self.anim_cachorro_esquerda, self.anim_cachorro_direita):
            imagens |= Inicializador.carregar_animacoes(lista)
            
        self.imagens_cachorro = imagens

        self.anim_pombo_esquerda = Inicializador.gerar_lista_animacoes("pombo", "fly_left", 4)
        self.anim_pombo_direita = Inicializador.gerar_lista_animacoes("pombo", "fly_right", 4)
        imagens = {}
        for lista in (self.anim_pombo_esquerda, self.anim_pombo_direita):
                    imagens |= Inicializador.carregar_animacoes(lista)

        self.imagens_pombos = imagens

        self.anim_chefe_idle_left = Inicializador.gerar_lista_animacoes("drm", "idle_left", 4)
        self.anim_chefe_idle_right = Inicializador.gerar_lista_animacoes("drm", "idle_right", 4)
        self.anim_chefe_walk_left = Inicializador.gerar_lista_animacoes("drm", "walk_left", 5)
        self.anim_chefe_walk_right = Inicializador.gerar_lista_animacoes("drm", "walk_right", 5)

        imagens = {}
        for lista in (self.anim_chefe_idle_left, self.anim_chefe_idle_right, 
                    self.anim_chefe_walk_left, self.anim_chefe_walk_right):
                imagens |= Inicializador.carregar_animacoes(lista)
                        
        self.imagens_chefe = imagens
        
        self.anim_jogador_idle_left = Inicializador.gerar_lista_animacoes("soldado", "idle_left", 4)
        self.anim_jogador_idle_right = Inicializador.gerar_lista_animacoes("soldado", "idle_right", 4)
        self.anim_jogador_walk_left = Inicializador.gerar_lista_animacoes("soldado", "walk_left", 4)
        self.anim_jogador_walk_right = Inicializador.gerar_lista_animacoes("soldado", "walk_right", 4)
        self.anim_jogador_jump_right = Inicializador.gerar_lista_animacoes("soldado", "jump_right", 3)
        self.anim_jogador_jump_left = Inicializador.gerar_lista_animacoes("soldado", "jump_left", 3)
        self.anim_jogador_to_look_up = Inicializador.gerar_lista_animacoes("soldado", "to_look_up", 4)

        imagens = {}
        for lista in (self.anim_jogador_idle_left, self.anim_jogador_idle_right, 
                      self.anim_jogador_walk_left, self.anim_jogador_walk_right,
                      self.anim_jogador_jump_right, self.anim_jogador_jump_left,
                      self.anim_jogador_to_look_up):
                    imagens |= Inicializador.carregar_animacoes(lista)
                
        self.imagens_jogador = imagens


    def carregar_fase(self, caminho):
        mapa = Inicializador.carregar_mapa(caminho)
        self.plataformas, self.blocks, self.coletaveis = Inicializador.criar_level(mapa)
        self.zumbis, self.cachorros, self.pombos, self.chefe = Inicializador.criar_inimigos(mapa, self.plataformas, self.blocks, self.gerenciadorFases.dificuldade)
        self.portais = [p for p in self.plataformas if p.tipo == "teleport"]
        self.largura_mapa = len(mapa[0]) * TAMANHO_QUADRADO
        self.altura_mapa = len(mapa) * TAMANHO_QUADRADO

        inimigos = self.zumbis + self.cachorros + self.pombos
        if self.chefe != None:
            inimigos += [self.chefe] 

        if self.gerenciadorFases.fase_atual == 0 and self.voltando == False:
            arma = Arma(60, POS_INICIO.copy(), AMARELO)
            self.jogador = Jogador(POS_INICIO.copy(), self.plataformas, inimigos, 
                                self.coletaveis, [arma], VERMELHO)
            self.jogador.tamanho = TAMANHO_JOGADOR
            self.jogador.image = self.anim_jogador_idle_right[0]
        else:
            self.jogador.plataformas = self.plataformas
            self.jogador.coletaveis = self.coletaveis
            self.jogador.inimigos = inimigos

        self.camera = Camera(self.jogador, self.largura_mapa, self.altura_mapa)

        for z in self.zumbis:
            z.image = self.anim_zumbi_idle_direita[0]
            z.inimigos.append(self.jogador)

        for c in self.cachorros:
            c.image = self.anim_cachorro_idle[0]
            c.inimigos.append(self.jogador)

        for p in self.pombos:
            p.image = self.anim_pombo_esquerda[0]
            p.inimigos.append(self.jogador)

        if self.chefe != None:
            self.chefe.image = self.anim_chefe_idle_left[0]
            self.chefe.jogador = self.jogador

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
        #faulthandler.dump_traceback_later(5, repeat=True)
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

    def reiniciar(self):
         self.jogador.resetar(POS_INICIO)
         self.jogador.vida = 100
         self.jogador.pontuacao = 0
         self.jogador.quantidade_coletada = 0
         self.jogador.tempo = 0

         self.gerenciadorFases.reiniciar()
         self.estado_jogo = "jogando"

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                
            if self.estado_jogo == "menu":
                    acao = acao_menu(evento, pygame.mouse.get_pos())
                    if acao == "jogar":
                        self.estado_jogo = "jogando"
                        self.gerenciadorFases.definir_dificuldade(get_dificuldade())
                        self.carregar_sprites()
                        self.carregar_fase(self.gerenciadorFases.caminho_fase_atual())
                    elif acao == "sair":
                        self.rodando = False

            elif self.estado_jogo == "jogando":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_h:
                        self.debug = not self.debug

                    elif evento.key == pygame.K_w:
                        self.estado_jogo = "win"

                    elif evento.key == pygame.K_g:
                        self.estado_jogo = "gameover"

            elif self.estado_jogo == "win" or self.estado_jogo == "gameover":
                 acao = acao_tela_final(evento)
                 if acao == "reiniciar":
                      self.reiniciar()
                 elif acao == "menu":
                      self.estado_jogo = "menu"
                
    # Atualização
    def atualizar(self, dt):
        if self.estado_jogo == "jogando":
            Atualizador.atualizar_jogador(self, dt)
            self.camera.atualizar()
            Atualizador.atualizar_animacao(self, dt)
            Atualizador.atualizar_entidades(self, dt)
            self.gerenciadorFases.verificar_conclusao(self)

    # Renderização
    def desenhar(self):
        #comeca desenhando o menu q é o estado inicial do jogo
        if self.estado_jogo == "menu":
            desenhar_menu(self.tela, (pygame.mouse.get_pos()))

        #comeca o jogo apenas se o estado foi alterado para "jogando" a partir do retorno de acao_menu
        elif self.estado_jogo == "jogando":
            x_camera = abs(self.camera.retangulo.x)
            desenhar_cenario(self.tela, x_camera, self.gerenciadorFases.fase_atual)
            # self.tela.fill(AZUL_NOTURNO)
            self.tela.blit(self.mundo_surface, self.camera.retangulo.topleft)

            Renderizador.desenhar_portais(self)
            Renderizador.desenhar_coletaveis(self)
            Renderizador.desenhar_projeteis(self)
            Renderizador.desenhar_zumbis(self)
            Renderizador.desenhar_cachorros(self)
            Renderizador.desenhar_pombos(self)
            Renderizador.desenhar_chefe(self)
            Renderizador.desenhar_jogador(self)
            Renderizador.desenhar_hud(self)
            if self.debug:
                Renderizador.desenhar_aabb_de_portal(self)

        elif self.estado_jogo == "win" or self.estado_jogo == "gameover":
            x_camera = abs(self.camera.retangulo.x)
            desenhar_cenario(self.tela, x_camera, self.gerenciadorFases.fase_atual)
            # self.tela.fill(AZUL_NOTURNO)
            self.tela.blit(self.mundo_surface, self.camera.retangulo.topleft)

            Renderizador.desenhar_portais(self)
            Renderizador.desenhar_coletaveis(self)
            Renderizador.desenhar_projeteis(self)
            Renderizador.desenhar_zumbis(self)
            Renderizador.desenhar_cachorros(self)
            Renderizador.desenhar_pombos(self)
            Renderizador.desenhar_jogador(self)
            Renderizador.desenhar_hud(self)
            if self.debug:
                Renderizador.desenhar_aabb_de_portal(self)            

            desenhar_tela_final(self.tela, self.estado_jogo, self.jogador, self.fonte, self.fonte_titulo)

        pygame.display.flip()

if __name__ == "__main__":
    Jogo().rodar()