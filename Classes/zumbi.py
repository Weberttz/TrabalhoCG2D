import random
from Classes.humanoide import Humanoide

class Zumbi(Humanoide):
    def __init__(self, plataformas, pos, cor):
        super().__init__(plataformas, [], pos, cor)
        self.vertices = []
        self.tempo_mudar_direcao = 0

    def atualizar(self):
        self.aplicar_gravidade()
        self.lidar_com_colisoes()
        self.movimentar()
        self.vertices = [(self.pos.x, self.pos.y), 
                            (self.pos.x, self.pos.y - self.tamanho),
                            (self.pos.x + self.tamanho, self.pos.y - self.tamanho), 
                            (self.pos.x + self.tamanho, self.pos.y)]

    def movimentar(self):
        pos_base = 690
        controle = self.retangulo.x + self.vel_x * self.velocidade
        base = [p for p in self.plataformas if p.y0 == pos_base]

        # Move o zumbi baseado na direção atual
        self.retangulo.x += self.vel_x * self.velocidade

        # Diminui o contador e muda de direção aleatoriamente ao zerar
        self.tempo_mudar_direcao -= 1
        if self.tempo_mudar_direcao <= 0:
            self.vel_x = random.choice([-1, 0, 1])
            self.tempo_mudar_direcao = random.randint(30, 60)  # Quadros (Frames)