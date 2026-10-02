import random
from Classes.humanoide import Humanoide

class Cachorro(Humanoide):
    def __init__(self, plataformas, pos, equipamentos, cor):
        super().__init__(plataformas, [], equipamentos, pos, cor)
        self.vertices = []
        self.tempo_mudar_direcao = 0
        self.vivo = True
        self.dano = 10

    def atualizar(self):
        self.aplicar_gravidade()
        self.atualizar_vertices()
        self.lidar_com_colisoes()
        self.movimentar()

    def lidar_com_colisoes(self):
        for plataforma in self.plataformas:
            if plataforma.retangulo.colidiu_com(self.retangulo):
                self.vel_x = 0
        return super().lidar_com_colisoes()
    
    def movimentar(self):
        # Move o cachorro baseado na direção atual
        self.retangulo.x += self.vel_x * self.velocidade

        # Diminui o contador e muda de direção aleatoriamente ao zerar
        self.tempo_mudar_direcao -= 1
        if self.tempo_mudar_direcao <= 0:
            self.vel_x = random.choice([-1, 0, 1])
            self.tempo_mudar_direcao = random.randint(30, 60)  # Quadros (Frames)