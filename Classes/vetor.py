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
        return Vetor(self.x + outro.x, self.y + outro.y)

    def __mul__(self, escalar):           # vetor * número
        return Vetor(self.x * escalar, self.y * escalar)
    
    def pegar_tamanho(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalizar(self):
        tamanho = self.pegar_tamanho()
        if tamanho == 0:
            raise ValueError("não dá para normalizar o vetor zero")
        return Vetor(self.x / tamanho, self.y / tamanho)

    def angulo_para(self, outro):
        # Calcula angulo para o vetor de destino
        angulo = math.degrees(math.atan2(outro[1], outro[0]) -
                              math.atan2(self.y, self.x))
        return (angulo + 180) % 360 - 180          # mantém em [-180, 180]

