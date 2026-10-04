from settings import Retangulo
class Coletavel():
    def __init__(self, pos, largura, altura, cor, tipo, forma = "retangular"):
        self.tipo = tipo
        self.pos = pos
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.forma = forma
        self.ativo = True
        self.retangulo = Retangulo(self.pos.x, self.pos.y, largura, altura)
        self.centro = None
        self.raio = None
        self.converter()
    
    def converter(self):
        """Caso o coletável seja circular, esse método faz conversão de retangulo para circunferência"""
        aux = 16 # largura_QUADRADO // 2
        self.raio = self.largura
        self.centro = (self.pos.x + aux, self.pos.y)
        if self.forma == "circular":
            canto_x = self.centro[0] - self.raio 
            canto_y = self.centro[1] - self.raio
            diametro = 2 * self.raio
            
            self.retangulo = Retangulo(canto_x, canto_y, diametro, diametro)