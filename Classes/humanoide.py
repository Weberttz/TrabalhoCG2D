from settings import *

class Humanoide(pygame.sprite.Sprite): 
    def __init__(self, plataformas, inimigos, equipamentos, pos, cor):
        self.vida = 100
        self.cor = cor
        self.tamanho = 30
        self.equipamentos = equipamentos

        if len(equipamentos) > 0:
            self.equipamento = equipamentos[0]
        else: self.equipamento = None

        # Física
        self.pos = pos # pygame.Vector2(100, 300)
        self.vel_x = 0
        self.vel_y = 0
        self.aceleracao = pygame.Vector2(0, 10)
        self.no_chao = False

        self.retangulo = pygame.Rect(self.pos.x, self.pos.y - self.tamanho, self.tamanho, self.tamanho)

        # Movimento
        self.velocidade = 5
        self.forca_pulo = -15
        self.plataformas = plataformas
        self.inimigos = inimigos

        self.frame = 0
        self.image = None

    def aplicar_gravidade(self):
        # aplicar gravidade se não estiver no chão
        self.aceleracao.y += 0.8
        if self.aceleracao.y > 10: # Aceleração tem teto
            self.aceleracao.y = 10

    def atualizar_vertices(self):
         self.vertices = [(self.pos.x, self.pos.y), 
                                    (self.pos.x, self.pos.y - self.tamanho),
                                    (self.pos.x + self.tamanho, self.pos.y - self.tamanho), 
                                    (self.pos.x + self.tamanho, self.pos.y)]

    def atualizar_vertices_equipamento(self):
        if self.equipamento != None:
            pos_equipamento_x = self.pos.x + self.tamanho
            pos_equipamento_y = self.pos.y - self.tamanho // 2
            self.equipamento.vertices = [(pos_equipamento_x, pos_equipamento_y), 
                                            (pos_equipamento_x, pos_equipamento_y - self.equipamento.altura),
                                            (pos_equipamento_x + self.equipamento.largura, pos_equipamento_y - self.equipamento.altura), 
                                            (pos_equipamento_x + self.equipamento.largura, pos_equipamento_y)]
                    
    def lidar_com_colisoes(self):
        # Movimento horizontal
        self.pos.x += self.vel_x
        self.retangulo.x = self.pos.x
        
        objetos = self.plataformas + self.inimigos

        # Colisão com eixo X
        for plataforma in objetos:
            if self.retangulo.colliderect(plataforma.retangulo):
                if self.vel_x > 0:  # Movendo para a direita
                    self.retangulo.right = plataforma.retangulo.left
                elif self.vel_x < 0:  # Movendo para a esquerda
                    self.retangulo.left = plataforma.retangulo.right
                self.pos.x = self.retangulo.x # Sincroniza a posição com o eixo x do obstáculo

        # Movimento vertical
        self.pos.y += self.aceleracao.y
        self.retangulo.y = self.pos.y  

        self.no_chao = False

        for plataforma in objetos:
            if self.retangulo.colliderect(plataforma.retangulo):
                if self.aceleracao.y > 0:  # Caindo
                    self.retangulo.bottom = plataforma.retangulo.top
                    self.no_chao = True
                    self.aceleracao.y = 0
                elif self.aceleracao.y < 0:  # Pulando
                    self.retangulo.top = plataforma.retangulo.bottom
                    self.aceleracao.y = 0
                self.pos.y = self.retangulo.y # Sincroniza a posição com o eixo y do obstáculo


    def animar(self, lista_idle, lista_walk_left, lista_walk_right):
        if self.vel_x == 0 and self.vel_y == 0:
            self.mudar_frame(lista_idle)
        elif self.vel_x < 0:
            self.mudar_frame(lista_walk_right)
        else:
            self.mudar_frame(lista_walk_left)

    def mudar_frame(self, lista_animacao):
        # Avança para o próximo quadro da animação
        # O operador '%' (módulo) faz com que a contagem volte a 0 quando chegar ao fim da lista.
        self.frame = (self.frame + 1) % len(lista_animacao)
        
        # Atualiza a imagem do herói para a imagem do quadro atual.
        self.image = lista_animacao[self.frame]