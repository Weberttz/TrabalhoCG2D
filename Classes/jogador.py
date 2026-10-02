import pygame 
from Classes.humanoide import Humanoide
from settings import Vetor, Retangulo

class Jogador(Humanoide):
    def __init__(self, pos, plataformas, inimigos, coletaveis, equipamentos, cor):
        super().__init__(plataformas, inimigos, equipamentos, pos, cor)
        self.tempo = pygame.time.get_ticks()
        self.olhando = 1
        self.coletaveis = coletaveis
        self.quantidade_coletada = 0
        self.invulneravel = False
        self.tempo_invulnerabilidade = 1.0          # 1 seg
        self.momento_ultimo_dano = 0

    def resetar(self, pos_inicial):
        self.pos = pos_inicial.copy()
        self.vel_x = 0
        self.vel_y = 0
        self.aceleracao = Vetor(0, 10) 
        self.no_chao = False
        # self.vida = 100
        self.retangulo = Retangulo(self.pos.x, self.pos.y - self.tamanho,
                                self.tamanho, self.tamanho)
        self.atualizar_vertices()

    def atualizar(self):
        '''Atualiza os atributos do jogador.'''
        self.lidar_com_inputs()
        self.aplicar_gravidade()
        self.atualizar_vertices()
        self.lidar_com_colisoes()
        self.atualizar_vertices_equipamento()
        self.atirar()
        self.atualizar_invulnerabilidade()

    def get_direcao_tiro(self):
        '''Determina a direção do tiro.'''
        keys = pygame.key.get_pressed()

        x = 0
        if keys[pygame.K_RIGHT]: x += 1
        if keys[pygame.K_LEFT]:  x -= 1

        y = 0
        if keys[pygame.K_UP] and x == 0:   y -= 1    # cima
        # if keys[pygame.K_DOWN] and not self.no_chao: y += 1  # baixo só no ar

        if x == 0 and y == 0:
            x = self.olhando              # parado: atira para onde olha

        direcao = Vetor(x, y)
        return direcao.normalizar()

    def atirar(self):
        '''Recebe comandos de teclado para atirar projéteis.
           \nArma acionada pela tecla : Z  
        '''
        pos = Vetor(self.pos.x + self.tamanho // 2,
                            self.pos.y - self.tamanho // 2 - self.equipamento.altura)

        tempo = pygame.time.get_ticks()
        if tempo - self.equipamento.tempo >= self.equipamento.intervalo_tiro:
            self.equipamento.tempo = tempo
            self.equipamento.pode_atirar = True

        if pygame.key.get_pressed()[pygame.K_z]:
            self.equipamento.atacar(self.get_direcao_tiro(), pos)

    def lidar_com_inputs(self):
        '''Recebe comandos de teclado para mover o jogador. 
            \nLEFT - volta para o começo do mapa
            \nRIGHT - segue para o fim do mapa
            \nSPACE - pula
        '''
        keys = pygame.key.get_pressed()

        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x += -self.velocidade
            self.olhando = -1
    
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.velocidade
            self.olhando = 1

        if keys[pygame.K_SPACE] and self.no_chao:
            self.aceleracao.y = self.forca_pulo
            self.no_chao = False

    def lidar_com_colisoes(self):

        self.colidir_com_coletavel()
        self.colidir_com_inimigo()

        return super().lidar_com_colisoes()
    
    def colidir_com_coletavel(self):
        '''Trata colisão com coletáveis'''
        for coletavel in self.coletaveis:
            if self.retangulo.colidiu_com(coletavel.retangulo) and coletavel.ativo:
                if coletavel.tipo == "tapioca":
                    self.vida+= 30 
                if coletavel.tipo == "municao":
                    self.equipamento.municao+=1
                        
                self.quantidade_coletada += 1
                coletavel.ativo = False   
    
    def colidir_com_inimigo(self):
        '''Trata colisão com inimigos''' 
        for inimigo in self.inimigos:
            if self.retangulo.colidiu_com(inimigo.retangulo) and not self.invulneravel:
                self.vida -= inimigo.dano
                self.invulneravel = True
                self.momento_ultimo_dano = pygame.time.get_ticks() 

    def atualizar_invulnerabilidade(self):
        '''Verifica se já passou o tempo de invulnerabilidade:
        \n - se sim, torna vulnerável outra vez
        \n - se não, permanece invulnerável (não perde vida em colisões com inimigos)
        '''
        if self.invulneravel:
            if (pygame.time.get_ticks() - self.momento_ultimo_dano) >= self.tempo_invulnerabilidade * 1000:
                self.invulneravel = False