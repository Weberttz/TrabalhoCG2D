from settings import *

class Projetil(pygame.sprite.Sprite):
    def __init__(self, pos:pygame.Vector2, disparou_para:pygame.Vector2, bala_inimiga=False):
        super().__init__()
        self.pos = pos
        self.disparou_para = disparou_para
        self.imagem = pygame.surface.Surface((10,10)).convert()
        self.imagem.fill('yellow')
        self.retangulo = self.imagem.get_rect()
        self.retangulo.topleft = self.pos
        self.velocidade = 700
        self.direcao = pygame.Vector2(self.disparou_para.x - self.pos.x, self.disparou_para.y - self.pos.y)
        vec = pygame.Vector2(1,0)
        self.angulo = self.direcao.angle_to(vec)
        self.image = pygame.transform.rotate(self.imagem, self.angulo)
        if self.direcao.length != 0:
            self.direcao = self.direcao.normalize()

        self.bala_inimiga = bala_inimiga

        self.dano = 10 
        self.ativo = True
        self.time = 0
    
    def update(self,dt):
        self.pos += self.direcao * self.velocidade *dt
        self.pos = pygame.Vector2(self.pos)
        self.retangulo.topleft = self.pos

    def draw(self, superficie, scroll, camera):
        tolerancia = 500
        pos = self.pos - scroll
        if pos.x < -tolerancia or pos.x > LARGURA+tolerancia  or pos.y < -tolerancia or pos.y  >  ALTURA+tolerancia:
            self.ativo = False
        superficie.blit(self.image, camera.aplicar(self))