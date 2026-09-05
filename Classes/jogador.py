import pygame 

class Jogador:
    def __init__(self, plataformas, inimigos ,cor):
        self.vida = 100
        self.cor = cor
        self.tamanho = 30

        # Física
        self.pos = pygame.Vector2(100, 300)
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

    def atualizar(self):
        self.lidar_com_inputs()
        self.aplicar_gravidade()
        self.lidar_com_colisoes()

        self.vertices = [(self.pos.x, self.pos.y), 
                            (self.pos.x, self.pos.y - self.tamanho),
                            (self.pos.x + self.tamanho, self.pos.y - self.tamanho), 
                            (self.pos.x + self.tamanho, self.pos.y)]

    def lidar_com_inputs(self):
        keys = pygame.key.get_pressed()

        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x += -self.velocidade
    
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.velocidade

        if keys[pygame.K_SPACE] and self.no_chao:
            self.aceleracao.y = self.forca_pulo
            self.no_chao = False

    def aplicar_gravidade(self):
        # aplicar gravidade se não estiver no chão
        self.aceleracao.y += 0.8
        if self.aceleracao.y > 10: # Aceleração tem teto
            self.aceleracao.y = 10

    def lidar_com_colisoes(self):
        # Movimento horizontal
        self.pos.x += self.vel_x
        self.retangulo.x = self.pos.x

        for plataforma in self.plataformas:
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

        for plataforma in self.plataformas:
            if self.retangulo.colliderect(plataforma.retangulo):
                if self.aceleracao.y > 0:  # Caindo
                    self.retangulo.bottom = plataforma.retangulo.top
                    self.no_chao = True
                    self.aceleracao.y = 0
                elif self.aceleracao.y < 0:  # Pulando
                    self.retangulo.top = plataforma.retangulo.bottom
                    self.aceleracao.y = 0
                self.pos.y = self.retangulo.y # Sincroniza a posição com o eixo y do obstáculo

        for inimigo in self.inimigos:
            if self.retangulo.colliderect(inimigo.retangulo):
                inimigo.cor = "blue"
                self.vida-= 1
                if self.vida < 0: self.vida = 0
            else: inimigo.cor = "green"
            