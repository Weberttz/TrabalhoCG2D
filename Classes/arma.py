from Classes.equipamento import Equipamento

class Arma(Equipamento):
    def __init__(self, quantidade_uso, pos, cor):
        super().__init__(quantidade_uso, pos, cor, 20, 8)
