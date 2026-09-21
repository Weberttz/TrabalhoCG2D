class Retangulo():

    __slots__ = ("x", "y", "largura", "altura")

    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura

    def copy(self):
        return Retangulo(self.x, self.y, self.largura, self.altura)

    # para o interpretador saber a quantidade de atributos declarados
    def __len__(self):
        return 4

    # recolher um atributo do objeto
    def __getitem__(self, i):
        return (self.x, self.y, self.largura, self.altura)[i]

    # para poder interar e desempacotar os valores
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.largura
        yield self.altura


    # @property serve para usar o retorno do método como atributo 
    # daí não precisa guardar variáveis 
    @property
    def left(self):
        return self.x

    # setter para atribuir valores quando tiver colisão

    @left.setter
    def left(self, valor):
        self.x = valor

    @property
    def right(self):
        return self.x + self.largura

    @right.setter
    def right(self, valor):
        self.x = valor - self.largura

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, valor):
        self.y = valor

    @property
    def bottom(self):
        return self.y + self.altura

    @bottom.setter
    def bottom(self, valor):
        self.y = valor - self.altura

    @property
    def vertices(self):
        return [(self.left, self.top), (self.right, self.top),
                (self.right, self.bottom), (self.left, self.bottom)]

    @property
    def topleft(self):
        return (self.x, self.y)
 
    @topleft.setter
    def topleft(self, pos):
        self.x, self.y = pos[0], pos[1]
 
    @property
    def bottomleft(self):
        return (self.x, self.bottom)
 
    @bottomleft.setter
    def bottomleft(self, pos):
        self.x, self.bottom = pos[0], pos[1]
 
    @property
    def topright(self):
        return (self.right, self.y)
 
    @topright.setter
    def topright(self, pos):
        self.right, self.y = pos[0], pos[1]
 
    @property
    def bottomright(self):
        return (self.right, self.bottom)
 
    @bottomright.setter
    def bottomright(self, pos):
        self.right, self.bottom = pos[0], pos[1]
 
    @property
    def centerx(self):
        return self.x + self.largura / 2
 
    @centerx.setter
    def centerx(self, valor):
        self.x = valor - self.largura / 2
 
    @property
    def centery(self):
        return self.y + self.altura / 2
 
    @centery.setter
    def centery(self, valor):
        self.y = valor - self.altura / 2
 
    @property
    def center(self):
        return (self.centerx, self.centery)
 
    @center.setter
    def center(self, pos):
        self.centerx, self.centery = pos[0], pos[1]

    # movimento do rect para simular camera e máscara de colisão
    def move(self, dx, dy=None):
        if dy is None:                         
            dx, dy = dx
        return Retangulo(self.x + dx, self.y + dy, self.largura, self.altura)

    def move_ip(self, dx, dy):
        self.x += dx
        self.y += dy

    # Colisão AABB

    @staticmethod
    def calcular_aabb(pontos):
        xs = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]
        
        return min(xs), min(ys), max(xs), max(ys)

    @staticmethod
    def colisao_aabb(a, b):
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        
        return (
            ax1 < bx2 and
            ax2 > bx1 and
            ay1 < by2 and
            ay2 > by1
        )

    def colidiu_com(self, outro):
        a = self.calcular_aabb(self.vertices)
        b = self.calcular_aabb(outro.vertices)
        return self.colisao_aabb(a, b)
