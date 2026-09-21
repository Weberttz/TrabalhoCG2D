from settings import *

class Projetil(pygame.sprite.Sprite):
    def __init__(self, pos:Vetor, disparou_para:Vetor, bala_inimiga=False):
        super().__init__()
        self.pos = pos
        self.disparou_para = disparou_para
        self.imagem = pygame.surface.Surface((10,10)).convert()
        self.imagem.fill('white')
        self.retangulo = Retangulo(pos.x, pos.y, 10, 10)
        self.retangulo.topleft = self.pos
        self.velocidade = 400
        self.direcao = Vetor(self.disparou_para.x - self.pos.x, self.disparou_para.y - self.pos.y)
        vec = Vetor(1,0)

        self.angulo = self.direcao.angulo_para(vec)
        self.image = pygame.transform.rotate(self.imagem, self.angulo)

        if self.direcao.pegar_tamanho() != 0:
            self.direcao = self.direcao.normalizar()

        self.bala_inimiga = bala_inimiga

        self.dano = 30 
        self.ativo = True
        self.time = 0
    
    def atualizar(self,dt, plataformas):
        self.pos += self.direcao * self.velocidade *dt
        self.pos = Vetor(self.pos)
        self.retangulo.topleft = self.pos
        self.checar_colisao_com_plataforma(plataformas)

    def checar_colisao_com_plataforma(self, plataformas):
        for plataforma in plataformas:
            if plataforma.retangulo.colidiu_com(self.retangulo):
                self.ativo = False

    def desenhar(self, superficie, scroll, camera):
        tolerancia = 500
        pos = self.pos - scroll
        if pos.x < -tolerancia or pos.x > LARGURA+tolerancia  or pos.y < -tolerancia or pos.y  >  ALTURA+tolerancia:
            self.ativo = False
        superficie.blit(self.image, camera.aplicar(self))