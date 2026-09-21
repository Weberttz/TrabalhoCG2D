from Classes.coletavel import Coletavel
from settings import Retangulo
import math

class Tapioca(Coletavel):
    def __init__(self, centro, raio, cor):
        super().__init__(centro, raio, cor, "tapioca")
        self.centro = centro
        self.raio = raio
        self.cor = cor
        self.retangulo = Retangulo(self.centro.x - math.sqrt(raio), self.centro.y, raio, raio)