import pygame 
from Classes.humanoide import Humanoide
from Classes.vetor import Vetor

class Jogador(Humanoide):
    def __init__(self, pos, plataformas, inimigos, coletaveis, equipamentos, cor):
        super().__init__(plataformas, inimigos, equipamentos, pos, cor)
        self.tempo = pygame.time.get_ticks()
        self.olhando = 1
        self.coletaveis = coletaveis
        self.quantidade_coletada = 0

    def atualizar(self):
        self.lidar_com_inputs()
        self.aplicar_gravidade()
        self.atualizar_vertices()
        self.lidar_com_colisoes()
        self.atualizar_vertices_equipamento()
        self.atirar()

    def get_direcao_tiro(self):
        keys = pygame.key.get_pressed()

        x = 0
        if keys[pygame.K_RIGHT]: x += 1
        if keys[pygame.K_LEFT]:  x -= 1

        y = 0
        if keys[pygame.K_UP]:   y -= 1    # cima
        if keys[pygame.K_DOWN] and not self.no_chao: y += 1  # baixo só no ar

        if x == 0 and y == 0:
            x = self.olhando              # parado: atira para onde olha

        direcao = Vetor(x, y)
        return direcao.normalizar()

    def atirar(self):
        pos = Vetor(self.pos.x + self.tamanho // 2,
                            self.pos.y - self.tamanho // 2 - self.equipamento.altura)

        tempo = pygame.time.get_ticks()
        if tempo - self.equipamento.tempo >= self.equipamento.intervalo_tiro:
            self.equipamento.tempo = tempo
            self.equipamento.pode_atirar = True

        if pygame.key.get_pressed()[pygame.K_z]:
            self.equipamento.atacar(self.get_direcao_tiro(), pos)

    def lidar_com_inputs(self):
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
        for coletavel in self.coletaveis:
            if self.retangulo.colidiu_com(coletavel.retangulo) and coletavel.ativo:
                self.quantidade_coletada += 1
                coletavel.ativo = False
        return super().lidar_com_colisoes()
    