import pygame 
from Classes.humanoide import Humanoide

class Jogador(Humanoide):
    def __init__(self, plataformas, inimigos , cor):
        pos = pygame.Vector2(100, 300)
        super().__init__(plataformas, inimigos, pos, cor)

    def atualizar(self):
        self.lidar_com_inputs()
        self.aplicar_gravidade()
        self.lidar_com_colisoes()

        self.vertices = [(self.pos.x, self.pos.y), 
                            (self.pos.x, self.pos.y - self.tamanho),
                            (self.pos.x + self.tamanho, self.pos.y - self.tamanho), 
                            (self.pos.x + self.tamanho, self.pos.y)]

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
