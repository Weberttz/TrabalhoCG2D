from settings import Retangulo
class Coletavel():
    def __init__(self, pos, tamanho, cor, tipo):
        self.tipo = tipo
        self.pos = pos
        self.tamanho = tamanho
        self.cor = cor
        self.ativo = True
        self.retangulo = Retangulo(self.pos.x, self.pos.y, tamanho, tamanho)
        self.centro = None
        self.raio = None
        self.converter()
    
    def converter(self):
        aux = 6
        self.raio = self.tamanho
        self.centro = (self.pos.x + 16, self.pos.y)
        if self.tipo == "tapioca" or self.tipo == "moeda":
            canto_x = self.centro[0] - self.raio 
            canto_y = self.centro[1] + self.raio - self.raio // 2
            diametro = 2 * self.raio
            
            self.retangulo = Retangulo(canto_x, canto_y, diametro, diametro)