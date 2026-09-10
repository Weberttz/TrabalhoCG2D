class Equipamento:
    def __init__(self, quantidade_uso, pos, cor, largura, altura):
        self.quantidade_uso = quantidade_uso
        self.cor = cor
        self.pos = pos
        self.vertices = []
        self.largura = largura
        self.altura = altura
        