import pygame 

class Jogador:
    def __init__(self, plataformas ,cor):
        self.vida = 3
        self.cor = cor
        self.tamanho = 30

        # Física
        self.pos = pygame.Vector2(100, 40)
        self.aceleracao = pygame.Vector2(0, 10)
        self.no_chao = False

        # Movimento
        self.velocidade = 5
        self.forca_pulo = -100
        self.plataformas = plataformas

    def atualizar(self):
        self.lidar_com_inputs()
        self.aplicar_gravidade()
        self.lidar_com_colisoes()

        self.vertices = [(self.pos.x, self.pos.y), 
                            (self.pos.x + self.tamanho, self.pos.y), 
                            (self.pos.x + self.tamanho, self.pos.y - self.tamanho), 
                            (self.pos.x, self.pos.y - self.tamanho)]

    def lidar_com_inputs(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.pos.x += -self.velocidade
    
        if keys[pygame.K_RIGHT]:
            self.pos.x += self.velocidade

        if keys[pygame.K_SPACE] and self.no_chao:
            self.pos.y += self.forca_pulo
            self.no_chao = False

    def aplicar_gravidade(self):
        # aplicar gravidade se não estiver no chão
        if not self.no_chao: 
            self.pos.y += self.aceleracao.y

    def lidar_com_colisoes(self):
        self.no_chao = False
        for plataforma in self.plataformas:
           for (x, y) in plataforma.vertices:
                valor1 = plataforma.x0 - self.tamanho
                valor2 = plataforma.x1
                if self.pos.y == y and  valor1 < self.pos.x and valor2 > self.pos.x: 
                    self.no_chao = True