from settings import *
import Biblioteca.algoritmos as bibgraf

class Projetil():
    def __init__(self, pos:Vetor, disparou_para:Vetor, cor,bala_inimiga=False, image = None):
        super().__init__()
        self.cor = cor
        self.pos = pos
        self.disparou_para = disparou_para
        self.pos_incial = pos
        self.image = image
        self.retangulo = Retangulo(pos.x, pos.y, 10, 10)
        if image is not None:
            self.retangulo = Retangulo(pos.x, pos.y, 32, 32)
        
        self.retangulo.topleft = self.pos
        self.velocidade = 400
        self.aceleracao = Vetor(0,10)
        self.direcao = Vetor(self.disparou_para.x - self.pos.x, 
                             self.disparou_para.y - self.pos.y)
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
        '''Desenha projetil e desativa ele se percorrer a distância máxima sem colidir com nada.'''
        # tolerancia = distancia maxima que o projetil vai percorrer se não colidir com nada antes 
        tolerancia = 12 * TAMANHO_QUADRADO
        novo_vetor = self.pos_incial - self.pos
        distancia = novo_vetor.calcular_norma()

        vertices = camera.aplicar_vertices(self.retangulo.vertices)

        if distancia > tolerancia:
            self.ativo = False
       
        if self.image != None:
            bibgraf.scanline_texture(superficie, vertices, self.uvs, self.image)
            return

        x_min = min(x for x, y in vertices)
        y_min = min(y for x, y in vertices)
        
        bibgraf.desenhar_circulo(superficie,(x_min + 5, y_min + 5), 4, self.cor, True)