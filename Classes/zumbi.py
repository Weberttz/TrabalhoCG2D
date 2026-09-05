from Classes.bloco import Objeto

class Zumbi(Objeto):
    def __init__(self, x, y, largura, altura, cor):
        self.vida = 3
        self.altura = altura
        self.largura = largura
        self.x = x
        self.y = y
        super().__init__(x, y, largura, altura, cor)
        self.vertices = []

    def atualizar(self):
            self.vertices = [(self.x, self.y), 
                                (self.x + self.altura, self.y), 
                                (self.x + self.altura, self.y - self.altura), 
                                (self.x, self.y - self.altura)]
