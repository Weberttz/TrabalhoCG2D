class Jogador:
    def __init__(self, cor):
        self.cor = cor
        self.tamanho = 30
        self.x = 0
        self.y = 40
        self.vel = 5
        self.pulando = False
        self.no_chao = False