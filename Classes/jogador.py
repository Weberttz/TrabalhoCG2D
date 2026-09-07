import pygame 
from Classes.humanoide import Humanoide

class Jogador(Humanoide):
    def __init__(self, pos, plataformas, inimigos, equipamentos, cor):
        super().__init__(plataformas, inimigos, equipamentos, pos, cor)

    def atualizar(self):
        self.lidar_com_inputs()
        self.aplicar_gravidade()
        self.lidar_com_colisoes()
        self.atualizar_vertices()
        self.atualizar_vertices_equipamento()

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
