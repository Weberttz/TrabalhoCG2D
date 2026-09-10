from settings import *
from Classes.equipamento import Equipamento
from Classes.projetil import Projetil

class Arma(Equipamento):
    def __init__(self, quantidade_uso, pos, cor):
        super().__init__(quantidade_uso, pos, cor, 20, 8)
        self.municao = 100
        self.pode_atirar = True
        self.projetils = []
        self.tempo = pygame.time.get_ticks()
        self.intervalo_tiro = 1000

    def atacar(self, mouse_pos, scroll, pos):
        keys = pygame.key.get_pressed()
        if self.pode_atirar:
            if (pygame.mouse.get_pressed()[0]) and self.municao > 0:
                projetil = Projetil(pygame.Vector2(pos),
                                mouse_pos + scroll)

                self.projetils.append(projetil)
                # self.shoot_sound.play()
                self.pode_atirar = False
                self.municao -= 1