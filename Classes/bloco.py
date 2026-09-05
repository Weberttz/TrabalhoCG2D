import pygame

class Objeto():
    def __init__(self, x0, y0, largura, altura, cor):
        self.cor = cor
        self.retangulo = pygame.Rect(x0, y0, largura, altura)