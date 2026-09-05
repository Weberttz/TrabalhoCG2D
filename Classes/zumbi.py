from Classes.humanoide import Humanoide

class Zumbi(Humanoide):
    def __init__(self, plataformas, pos, cor):
        super().__init__(plataformas, [], pos, cor)
        self.vertices = []

    def atualizar(self):
        self.aplicar_gravidade()
        self.lidar_com_colisoes()

        self.vertices = [(self.pos.x, self.pos.y), 
                            (self.pos.x, self.pos.y - self.tamanho),
                            (self.pos.x + self.tamanho, self.pos.y - self.tamanho), 
                            (self.pos.x + self.tamanho, self.pos.y)]
