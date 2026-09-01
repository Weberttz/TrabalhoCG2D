class Plataforma:
    def __init__(self, x0, x1, y0, y1, cor):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.vertices = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]
        self.cor = cor


    