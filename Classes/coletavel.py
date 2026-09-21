from settings import Retangulo
class Coletavel():
    def __init__(self, pos, tamanho, cor, tipo):
        self.tipo = tipo
        self.pos = pos
        self.tamanho = tamanho
        self.cor = cor
        self.ativo = True
        self.retangulo = Retangulo(self.pos.x, self.pos.y, tamanho, tamanho)
        