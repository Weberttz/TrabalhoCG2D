import pygame 
from Classes.humanoide import Humanoide

class Jogador(Humanoide):
    def __init__(self, pos, plataformas, inimigos, equipamentos, cor):
        super().__init__(plataformas, inimigos, equipamentos, pos, cor)
        self.tempo = pygame.time.get_ticks()

    def atualizar(self):
        self.lidar_com_inputs()
        self.aplicar_gravidade()
        self.lidar_com_colisoes()
        self.atualizar_vertices()
        self.atualizar_vertices_equipamento()
        self.atirar()

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return pygame.Vector2(x, y)

    def atirar(self):
        pos = pygame.Vector2(self.pos.x + self.tamanho , self.pos.y - self.tamanho - self.equipamento.altura)
        tempo = pygame.time.get_ticks()
        if tempo - self.equipamento.tempo >= self.equipamento.intervalo_tiro:
            self.equipamento.tempo = pygame.time.get_ticks()
            self.equipamento.pode_atirar = True

        self.equipamento.atacar(self.get_mouse_pos(), pygame.Vector2(0, 0), pos)
        # self.bullets.update(dt)


    def lidar_com_inputs(self):
        keys = pygame.key.get_pressed()

        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x += -self.velocidade
    
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.velocidade

        if keys[pygame.K_SPACE] and self.no_chao:
            self.aceleracao.y = self.forca_pulo
            self.no_chao = False
