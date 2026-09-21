from Classes.coletavel import Coletavel

class Tapioca(Coletavel):
    def __init__(self, centro, raio, cor):
        super().__init__(centro, raio, cor, "tapioca")
        self.centro = centro
        self.raio = raio
        self.cor = cor
        