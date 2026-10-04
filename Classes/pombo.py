from settings import TAMANHO_QUADRADO, Vetor, Retangulo, pygame, random, LARGURA, CINZA
from Classes.projetil import Projetil

class Pombo():
    def __init__(self, plataformas, pos, cor, nivel_dificuldade):
        self.tempo = pygame.time.get_ticks()
        self.plataformas = plataformas
        self.pos = pos
        self.cor = cor
        self.tamanho = 30
        self.vertices = []
        self.pedras = []
        self.inimigos = []
        self.retangulo = Retangulo(self.pos.x, self.pos.y - self.tamanho, self.tamanho, self.tamanho)
        self.atualizar_vertices()

        self.vida = 100
        self.vel_x = 0
        self.vel_y = 0
        self.velocidade = 10
        self.aceleracao = Vetor(0, 10)

        self.intervalo_lancamento_pedra = 2
        self.pode_lancar = True
        self.tempo_mudar_direcao = 0
        self.vivo = True
        self.dano = self.definir_dano(nivel_dificuldade)
        self.campo_de_visao = 20 * TAMANHO_QUADRADO

    def definir_dano(self,nivel_dificuldade):
        '''Define o dano do inimigo pelo nível de dificuldade escolhido pelo jogador.'''
        if nivel_dificuldade == None:
            return 10
        elif nivel_dificuldade == 'facil':
            return 10
        elif nivel_dificuldade == 'medio':
            return 20
        elif nivel_dificuldade == 'dificil':
            return 40

    def morrer(self):
        if self.vida == 0: self.vivo = False

    def checar_atingido(self, projeteis):
        for projetil in projeteis:
            if projetil.retangulo.colidiu_com(self.retangulo):
                self.vida -= projetil.dano
                projetil.ativo = False
                if self.vida <= 0: self.vida = 0

    def atualizar(self, projeteis):
        self.atualizar_vertices()
        self.lidar_com_colisao()
        self.movimentar()
        self.checar_atingido(projeteis)
        self.morrer()
        self.atirar()
        self.atingiu_jogador()

    def atualizar_vertices(self):
            self.vertices = [(self.pos.x, self.pos.y), 
                                        (self.pos.x, self.pos.y - self.tamanho),
                                        (self.pos.x + self.tamanho, self.pos.y - self.tamanho), 
                                        (self.pos.x + self.tamanho, self.pos.y)]

    def atingiu_jogador(self):
        jogador = self.inimigo
        for pedra in self.pedras:
            if pedra.retangulo.colidiu_com(jogador.retangulo):
                pedra.ativo = False
                jogador.vida -= self.dano
                jogador.invulneravel = True
                jogador.momento_ultimo_dano = pygame.time.get_ticks() 

        # assim que atingir o jogador, tiramos ela do array
        self.pedras[:] = [p for p in self.pedras if p.ativo]

    def atirar(self):
        jogador = self.inimigo
        tolerancia = TAMANHO_QUADRADO // 2
        delta_x = abs(self.pos.x -  jogador.pos.x)

        tempo = pygame.time.get_ticks()
        if tempo - self.tempo >= self.intervalo_lancamento_pedra * 1000: 
            self.tempo = tempo
            self.pode_lancar = True

        if self.pode_lancar and delta_x < tolerancia:
            pedra = Projetil(self.pos, jogador.pos, CINZA, True)
            self.pedras.append(pedra)
            self.pode_lancar = False

    def lidar_com_colisao(self):
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

        if self.pos.x < 0: self.pos.x = 0

    def movimentar(self):
        # Move o pombo baseado na direção atual
        self.inimigo = self.inimigos[0]

        # Diminui o contador e muda de direção aleatoriamente ao zerar
        self.tempo_mudar_direcao -= 1
        if self.tempo_mudar_direcao <= 0:
            esta_no_campo_de_visao = (abs(self.inimigo.pos.x - self.pos.x) < self.campo_de_visao)

            if esta_no_campo_de_visao:
                if self.inimigo.pos.x != self.pos.x:
                    self.vel_x = 2 * ((self.inimigo.pos.x - self.pos.x) / abs(self.inimigo.pos.x - self.pos.x))
                else:
                    self.vel_x = 0
            else: 
                self.vel_x = random.choice([-1, 0, 1])

            self.tempo_mudar_direcao = random.randint(30, 60)  # Quadros (Frames)
        