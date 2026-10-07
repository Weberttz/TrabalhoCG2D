from settings import *

class Humanoide(): 
    def __init__(self, plataformas, inimigos, equipamentos, pos, cor, tamanho):
        self.vida = 100
        self.cor = cor
        self.tamanho = tamanho
        self.equipamentos = equipamentos
        self.vertices = []
        self.olhando = 1

        if len(equipamentos) > 0:
            self.equipamento = equipamentos[0]
        else: self.equipamento = None

        # Física
        self.pos = pos
        self.vel_x = 0
        self.vel_y = 0
        self.aceleracao = Vetor(0, 10)
        self.no_chao = False

        self.retangulo = Retangulo(self.pos.x, self.pos.y - self.tamanho, self.tamanho, self.tamanho)
        self.atualizar_vertices()

        # Movimento
        self.velocidade = 5
        self.forca_pulo = -18
        self.plataformas = plataformas
        self.inimigos = inimigos

        self.frame = 0
        self.image = None

        self.tomando_dano = False
        self.tempo_dano = 0
        self.tempo_piscar = 5

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
        '''Trata colisões com as plataformas'''
        # Movimento horizontal
        self.pos.x += self.vel_x
        self.retangulo.x = self.pos.x
        
        objetos = [p for p in self.plataformas if not p.tipo == "teleport"]

        # Colisão com eixo X
        for objeto in objetos:
            if self.retangulo.colidiu_com(objeto.retangulo):
                if self.vel_x > 0:  # Movendo para a direita
                    self.retangulo.right = objeto.retangulo.left
                elif self.vel_x < 0:  # Movendo para a esquerda
                    self.retangulo.left = objeto.retangulo.right
                self.pos.x = self.retangulo.x # Sincroniza a posição com o eixo x do obstáculo

        # Movimento vertical
        self.pos.y += self.aceleracao.y
        self.retangulo.bottom = self.pos.y  

        self.no_chao = False

        # Colisão com eixo y
        for objeto in objetos:
            if self.retangulo.colidiu_com(objeto.retangulo):
                if self.aceleracao.y > 0:  # Caindo
                    self.retangulo.bottom = objeto.retangulo.top
                    self.no_chao = True
                    self.aceleracao.y = 0
                elif self.aceleracao.y < 0:  # Pulando
                    self.retangulo.top = objeto.retangulo.bottom
                    self.aceleracao.y = 0
                self.pos.y = self.retangulo.bottom # Sincroniza a posição com o eixo y do obstáculo

    def tomar_dano(self, tempo = 40):
        self.tomando_dano = True
        self.tempo_dano = tempo

    def animar(self, lista_idle_left, lista_idle_right, lista_walk_left, lista_walk_right):
        if self.vel_x == 0:
            if self.olhando == -1:
                self.mudar_frame(lista_idle_left)
            else:
                self.mudar_frame(lista_idle_right)
        elif self.vel_x < 0:
            self.mudar_frame(lista_walk_left)
        else:
            self.mudar_frame(lista_walk_right)

    def mudar_frame(self, lista_animacao):
        '''Avança para o próximo quadro da animação '''
        
        # O operador '%' (módulo) faz com que a contagem volte a 0 quando chegar ao fim da lista.
        self.frame = (self.frame + 1) % len(lista_animacao)
        
        # Atualiza a imagem do herói para a imagem do quadro atual.
        self.image = lista_animacao[self.frame]