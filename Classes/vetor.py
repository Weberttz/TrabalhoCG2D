from Biblioteca.transformacoes import produto_matriz
import math

class Vetor:
    __slots__ = ("x", "y")

    def __init__(self, x=0, y=None):
        if y is not None:                 # Vector2(3, 4)
            self.x, self.y = float(x), float(y)
        elif isinstance(x, (int, float)):  # Vector2(10) -> (10, 10)
            self.x = self.y = float(x)
        else:                              # Vector2((3, 4)) ou Vector2(outro_vetor)
            self.x, self.y = float(x[0]), float(x[1])

    def copy(self):
        return Vetor(self.x, self.y)

    def __len__(self):
        return 2

    def __getitem__(self, i):
        return (self.x, self.y)[i]

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, outro):
        return Vetor(self.x + outro[0], self.y + outro[1])

    def __mul__(self, escalar):           # vetor * número
        return Vetor(self.x * escalar, self.y * escalar)
    
    def __sub__(self, outro):
        return Vetor(self.x - outro[0], self.y - outro[1])

    def __neg__(self):
        return Vetor(-self.x, -self.y)
    
    def calcular_norma(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalizar(self):
        norma = self.calcular_norma()
        if norma == 0:
            raise ValueError("Não dá para normalizar o vetor nulo")
        return Vetor(self.x / norma, self.y / norma)

    def angulo_para(self, outro):
        # Calcula angulo para o vetor de destino
        angulo = math.degrees(math.atan2(outro[1], outro[0]) -
                              math.atan2(self.y, self.x))
        return (angulo + 180) % 360 - 180          # mantém em [-180, 180]

    def aplicar_transformacao(self, matriz):
        vetor = [self.x, self.y]
        v = produto_matriz(matriz,vetor)
        return Vetor(v[0],v[1])

