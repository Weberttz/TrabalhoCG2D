import pygame
from Classes.bloco import Objeto

class Plataforma(Objeto):
    def __init__(self, x0, y0, largura, altura, cor):
        x1 = x0 + largura
        self.y1 = y0 + altura
        self.x0 = x0
        super().__init__(x0, y0 + altura, largura, altura, cor)
        self.vertices = [(x0, y0), (x0, self.y1), (x1, self.y1), (x1, y0)]
        

# mudar a assinatura para Retangulo(left, top, largura, altura)
    