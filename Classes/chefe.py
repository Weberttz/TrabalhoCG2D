import pygame

from settings import TAMANHO_ZUMBI, TAMANHO_QUADRADO,random, CINZA
from Classes.vetor import Vetor
from Classes.retangulo import Retangulo
from Classes.humanoide import Humanoide
from Classes.projetil import Projetil

class Chefe(Humanoide):
    def __init__(self, plataformas, pos, cor, nivel_dificuldade):
        self.tamanho = TAMANHO_ZUMBI * 2
        super().__init__(plataformas, [],[] , pos, cor,self.tamanho)
        self.momento_ultimo_lancamento = pygame.time.get_ticks()
        self.plataformas = plataformas
        self.pos = pos
        self.cor = cor
        
        self.livros = []
        self.jogador = None
        self.retangulo = Retangulo(self.pos.x, self.pos.y - self.tamanho, self.tamanho, self.tamanho)
        self.atualizar_vertices()

        # podia exibir a vida do chefe tbm na tela final   
        self.vida = 400
        self.vel_x = 0
        self.vel_y = 0
        self.velocidade = 1 
        self.aceleracao = Vetor(0, 10)
            
        self.intervalo_lancamento_livro = 3
        self.pode_lancar = True
        self.tempo_mudar_direcao = 0
        self.vivo = True
        self.dano = self.definir_dano(nivel_dificuldade)
        self.campo_de_visao = 20 * TAMANHO_QUADRADO
        self.olhando = -1

        self.imagem_livro = pygame.image.load("Sprites/livro.png").convert_alpha()
        
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
                self.tomando_dano = True
                self.tomar_dano(10)
                if self.vida <= 0: self.vida = 0

    def atualizar(self,projeteis):
        self.aplicar_gravidade()
        self.atualizar_vertices()
        self.lidar_com_colisoes()
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
        '''Verifica se o livro atingiu o jogador.'''
        for livro in self.livros:
            if livro.retangulo.colidiu_com(self.jogador.retangulo):
                livro.ativo = False
                self.jogador.perder_vida(self.dano)
                self.jogador.tomar_dano(self.dano)
     
            # assim que atingir o jogador, tiramos ele do array
            self.livros[:] = [p for p in self.livros if p.ativo]
        
    def movimentar(self):
        '''Faz o inimigo ir em direção ao jogador.'''
        # Diminui o contador e muda de direção aleatoriamente ao zerar
        self.tempo_mudar_direcao -= 1

        # Distância horizontal até o inimigo
        distancia_x = self.jogador.pos.x - self.pos.x
        esta_no_campo_de_visao = abs(distancia_x) < self.campo_de_visao

        if esta_no_campo_de_visao:
        
            if distancia_x > 0:
                self.vel_x = self.velocidade
                self.olhando = 1

            elif distancia_x < 0:
                self.vel_x = - self.velocidade
                self.olhando = -1

            else:
                self.vel_x = 0

            return
        
        # Fora do campo de visão -> movimento aleatório
        self.tempo_mudar_direcao -= 1

        if self.tempo_mudar_direcao <= 0:
            self.vel_x = random.choice([-1, 0, 1])

            # Não coloca olhando = 0, variável para mudar sprite do zumbi
            if self.vel_x != 0:
                self.olhando = 1 if self.vel_x > 0 else -1

            self.tempo_mudar_direcao = random.randint(30, 60)
    
    def atirar(self):
        tolerancia = 12 * TAMANHO_QUADRADO
        delta_x = abs(self.pos.x - self.jogador.pos.x)

        tempo = pygame.time.get_ticks()
        if tempo - self.momento_ultimo_lancamento >= self.intervalo_lancamento_livro * 1000: 
            self.momento_ultimo_lancamento = tempo
            self.pode_lancar = True

        # cria o projetil e adiciona na lista - no Atualizador 
        if self.pode_lancar and delta_x <= tolerancia:
            livro = None
            # lançamento horizontal
            if self.jogador.retangulo.bottom >= self.retangulo.top:
                pos = Vetor(self.pos.x, self.pos.y - 2*self.tamanho/3)
                alvo = Vetor(self.jogador.pos.x, self.jogador.retangulo.top + self.jogador.tamanho/2)
                livro = Projetil(pos, alvo, CINZA, True, self.imagem_livro)
            # lancamento vertical
            else:
                pos = Vetor(self.pos.x + self.tamanho/2, self.pos.y - self.tamanho)
                livro = Projetil(pos, self.jogador.pos, CINZA, True, self.imagem_livro)
                
            self.livros.append(livro) 
            self.pode_lancar = False

    
   