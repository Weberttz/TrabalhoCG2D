import pygame

from Classes.humanoide import Humanoide

class Chefe(Humanoide):
    def __init__(self, pos, plataformas, inimigos, equipamentos, cor):
            super().__init__(plataformas, inimigos, equipamentos, pos, cor)
            self.tempo = pygame.time.get_ticks()
            self.olhando = 1
            self.quantidade_coletada = 0
            self.invulneravel = False
            self.tempo_invulnerabilidade = 1.0  # 1 seg
            self.momento_ultimo_dano = 0
            self.tempo_teleport = 4.0
            self.momento_ultimo_teleport = 100
            self.teleport_colidiu = None
            self.momento_entrada_teleport = None 

    def ia_chefe_ataque()
    