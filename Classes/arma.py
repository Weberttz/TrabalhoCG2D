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

    def atacar(self, direcao, pos):
        if self.pode_atirar and self.municao > 0:
            pos = pygame.Vector2(pos)
            projetil = Projetil(pos, pos + direcao)   # alvo = 1 unidade à frente
            self.projetils.append(projetil)
            self.pode_atirar = False
            self.municao -= 1