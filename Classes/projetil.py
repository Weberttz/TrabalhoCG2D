from settings import *
import Biblioteca.algoritmos as bibgraf

class Projetil():
    def __init__(self, pos:Vetor, disparou_para:Vetor, cor,bala_inimiga=False):
        super().__init__()
        self.pos = pos
        self.disparou_para = disparou_para
        self.pos_incial = pos
        self.image = pygame.surface.Surface((10,10)).convert() # ajeitar isso, se precisar
        self.image.fill(cor)
        self.retangulo = Retangulo(pos.x, pos.y, 10, 10)
        self.retangulo.topleft = self.pos
        self.velocidade = 400
        self.aceleracao = Vetor(0,10)
        self.direcao = Vetor(self.disparou_para.x - self.pos.x, self.disparou_para.y - self.pos.y)
        vec = Vetor(1,0)

        self.uvs = [
            (0, 1),  # inferior-esquerdo
            (0, 0),  # superior-esquerdo
            (1, 0),  # superior-direito
            (1, 1),  # inferior-direito
        ]

        self.angulo = self.direcao.angulo_para(vec)

        if self.direcao.calcular_norma() != 0:
            self.direcao = self.direcao.normalizar()

        self.bala_inimiga = bala_inimiga

        self.dano = 30 
        self.ativo = True
        self.time = 0

    # quem chama é o atualizador?
    def atualizar(self,dt, plataformas, trajetoria_obliquoa = False):
        if trajetoria_obliquoa:
            self.atualizar_trajetoria_obliquoa(dt,plataformas)
            return 
        
        self.pos += self.direcao * self.velocidade *dt
        self.pos = Vetor(self.pos)
        self.retangulo.topleft = self.pos
        self.checar_colisao_com_plataforma(plataformas)

    def atualizar_trajetoria_obliquoa(self, dt, plataformas):
        '''Trajetoria obliquoa para lançamentos do chefe'''
        # Movimento do projetil na eixo X
        if self.disparou_para.x > self.pos.x:
            direcao_x = 1
        else: 
            direcao_x = -1
        self.direcao = Vetor(direcao_x, -0.5)
        if self.direcao.calcular_norma() != 0:
            self.direcao = self.direcao.normalizar()

        self.pos += self.direcao * self.velocidade *dt
        #aplicar gravidade
        #self.pos.y += self.aceleracao.y

        #self.retangulo.bottom = self.pos.y
        #self.pos = Vetor(self.pos)
        self.retangulo.topleft = self.pos
        self.checar_colisao_com_plataforma(plataformas)
        
    
    def aplicar_gravidade(self):
            # aplicar gravidade se for lançamento obliquo
            self.aceleracao.y += 0.8
            if self.aceleracao.y > 10: # Aceleração tem teto
                self.aceleracao.y = 10
    
    def checar_colisao_com_plataforma(self, plataformas):
        for plataforma in plataformas:
            if plataforma.retangulo.colidiu_com(self.retangulo):
                self.ativo = False

    def desenhar(self, superficie, scroll, camera):
        '''Desenha projetil e desativa ele se percorrer a distância máxima sem colidir com nada.'''
        # tolerancia = distancia maxima que o projetil vai percorrer se não colidir com nada antes 
        tolerancia = 12 * TAMANHO_QUADRADO
        novo_vetor = self.pos_incial - self.pos
        distancia = novo_vetor.calcular_norma()

        vertices = camera.aplicar_vertices(self.retangulo.vertices)

        if distancia > tolerancia:
            self.ativo = False
            
        bibgraf.scanline_texture(superficie, vertices, self.uvs, self.image)