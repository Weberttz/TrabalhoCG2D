import pygame

from settings import TAMANHO_QUADRADO,random, CINZA
from Classes.vetor import Vetor
from Classes.retangulo import Retangulo
from Classes.humanoide import Humanoide
from Classes.projetil import Projetil

class Chefe(Humanoide):
    def __init__(self, plataformas, pos, cor, nivel_dificuldade):
        super().__init__(plataformas, [],[] , pos, cor)
        self.tempo = pygame.time.get_ticks()
        self.plataformas = plataformas
        self.pos = pos
        self.cor = cor
        self.tamanho = TAMANHO_QUADRADO * 2
        
        self.livros = []
        self.jogador = None
        self.retangulo = Retangulo(self.pos.x, self.pos.y - self.tamanho, self.tamanho, self.tamanho)
        self.atualizar_vertices()

        # podia exibir a vida do chefe tbm na tela final   
        self.vida = 60
        self.vel_x = 0
        self.vel_y = 0
        self.velocidade = 2
        self.aceleracao = Vetor(0, 10)
            
        self.intervalo_lancamento_livro = 4
        self.pode_lancar = True
        self.tempo_mudar_direcao = 0
        self.vivo = True
        self.dano = self.definir_dano(nivel_dificuldade)
        self.campo_de_visao = 30 * TAMANHO_QUADRADO
            
        self.momento_ultimo_dano = 0
        
    def definir_dano(self,nivel_dificuldade):
        '''Define o dano do inimigo pelo nível de dificuldade escolhido pelo jogador.'''
        if nivel_dificuldade == 'facil':
            return 30
        elif nivel_dificuldade == 'medio':
            return 35
        elif nivel_dificuldade == 'dificil':
            return 40

    def morrer(self):
        if self.vida == 0: self.vivo = False

    # podia fazer o dano do projetil aumentar por causa de algum coletável específico
    def checar_atingido(self, projeteis):
        '''Detecta se o chefe foi atingido e dimuinue a vida dele se tiver sido o caso.'''
        for projetil in projeteis:
            if projetil.retangulo.colidiu_com(self.retangulo):
                self.vida -= projetil.dano
                projetil.ativo = False
                print(f'Vida chefe: {self.vida}')
                if self.vida <= 0: self.vida = 0

    def atualizar(self,projeteis):
        self.aplicar_gravidade()
        self.atualizar_vertices()
        self.lidar_com_colisoes()
        self.movimentar()
        self.checar_atingido(projeteis)
        self.morrer()
        self.atirar()
    
    def atualizar_vertices(self):
            self.vertices = [(self.pos.x, self.pos.y), 
                                (self.pos.x, self.pos.y - self.tamanho),
                                (self.pos.x + self.tamanho, self.pos.y - self.tamanho), 
                                (self.pos.x + self.tamanho, self.pos.y)]
    
    def atingiu_jogador(self):
        '''Verifica se o livro atingiu o jogador.'''
        for livro in self.livros:
            if livro.retangulo.colidiu_com(self.jogador.retangulo):
                livro.ativo = False
                self.jogador.perder_vida(self.dano)
     
            # assim que atingir o jogador, tiramos ela do array
            self.livros[:] = [p for p in self.livros if p.ativo]
        
    def movimentar(self):
        '''Faz o inimigo ir em direção ao jogador.'''
        # Diminui o contador e muda de direção aleatoriamente ao zerar
        self.tempo_mudar_direcao -= 1
        if self.tempo_mudar_direcao <= 0:
            esta_no_campo_de_visao = (abs(self.jogador.pos.x - self.pos.x) < self.campo_de_visao)
    
            if esta_no_campo_de_visao:
                if self.jogador.pos.x != self.pos.x:
                    self.vel_x = self.velocidade * ((self.jogador.pos.x - self.pos.x) / abs(self.jogador.pos.x - self.pos.x))
                else:
                    self.vel_x = 0
            else: 
                self.vel_x = random.choice([-1, 0, 1])
    
            self.tempo_mudar_direcao = random.randint(30, 60)  # Quadros (Frames)
    
    def atirar(self):
        tolerancia = 10
        delta_x = abs(self.pos.x -  self.jogador.pos.x)

        tempo = pygame.time.get_ticks()
        if tempo - self.tempo >= self.intervalo_lancamento_livro * 1000: 
            self.tempo = tempo
            self.pode_lancar = True
    
        if self.pode_lancar and delta_x <= tolerancia:
            livro = Projetil(self.pos, self.jogador.pos, CINZA, True)
            self.livros.append(livro)
            self.pode_lancar = False
   