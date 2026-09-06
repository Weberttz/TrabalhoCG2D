import pygame

class Plataforma():
    def __init__(self, x0, y0, largura, altura, cor):
        self.cor = cor
        self.altura = altura
        self.x1 = x0 + largura
        self.y1 = y0 + altura
        self.x0 = x0
        self.y0 = y0
        self.retangulo = pygame.Rect(x0, self.y1, largura, altura)
        self.vertices = [(x0, y0), (x0, self.y1), (self.x1, self.y1), (self.x1, y0)]
        

# mudar a assinatura para Retangulo(left, top, largura, altura)
    