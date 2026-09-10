from settings import *

class Camera:
    def __init__(self, alvo, largura_mapa, altura_mapa):
        self.alvo = alvo
        self.altura_mapa = altura_mapa
        self.largura_mapa = largura_mapa
        self.camera = pygame.Rect(0, 0, LARGURA, ALTURA)

    def aplicar(self, entidade):
        return entidade.retangulo.move(self.camera.topleft)

    def aplicar_vertices(self, vertices):
        dx, dy = self.camera.topleft
        return [(x + dx, y + dy) for x, y in vertices]

    def atualizar(self):
        x = -self.alvo.retangulo.centerx + LARGURA // 2
        y = -self.alvo.retangulo.centery + ALTURA // 2
        
        # Limitar a câmera aos limites do mundo
        x = min(0, x)  # Lado esquerdo
        x = max(-(self.largura_mapa - LARGURA), x)  # Lado direito
        y = min(0, y)  # Topo
        y = max(-(self.altura_mapa - ALTURA), y)  # Base
        
        self.camera = pygame.Rect(x, y, self.largura_mapa, self.altura_mapa)
