import random
from Classes.humanoide import Humanoide

class Zumbi(Humanoide):
    def __init__(self, plataformas, pos, equipamentos, cor):
        super().__init__(plataformas, [], equipamentos, pos, cor)
        self.vertices = []
        self.tempo_mudar_direcao = 0
        self.vivo = True

    def atualizar(self, projetils):
        self.aplicar_gravidade()
        self.atualizar_vertices()
        self.lidar_com_colisoes()
        self.movimentar()
        self.atualizar_vertices_equipamento()
        self.checar_atingido(projetils)
        self.morrer()

    def morrer(self):
        if self.vida == 0: self.vivo = False

    def checar_atingido(self, projetils):
        for projetil in projetils:
            if projetil.retangulo.colidiu_com(self.retangulo):
                self.vida -= projetil.dano
                projetil.ativo = False
                if self.vida <= 0: self.vida = 0


    def lidar_com_colisoes(self):
        for plataforma in self.plataformas:
            if plataforma.retangulo.colidiu_com(self.retangulo):
                self.vel_x = 0
        return super().lidar_com_colisoes()
    
    def movimentar(self):
        # Move o zumbi baseado na direção atual
        self.retangulo.x += self.vel_x * self.velocidade

        # Diminui o contador e muda de direção aleatoriamente ao zerar
        self.tempo_mudar_direcao -= 1
        if self.tempo_mudar_direcao <= 0:
            self.vel_x = random.choice([-1, 0, 1])
            self.tempo_mudar_direcao = random.randint(30, 60)  # Quadros (Frames)