import pygame

from settings import TAMANHO_QUADRADO
from Classes.vetor import Vetor
from Classes.retangulo import Retangulo
from Classes.humanoide import Humanoide

class Chefe(Humanoide):
    def __init__(self, pos, plataformas, inimigos, equipamentos, cor, nivel_dificuldade):
        super().__init__(plataformas, inimigos, equipamentos, pos, cor)
        self.tempo = pygame.time.get_ticks()
        self.plataformas = plataformas
        self.pos = pos
        self.cor = cor
        self.tamanho = TAMANHO_QUADRADO * 2
        self.vertices = []
        self.pedras = []
        self.jogador = []
        self.retangulo = Retangulo(self.pos.x, self.pos.y - self.tamanho, self.tamanho, self.tamanho)
        self.atualizar_vertices()
            
        self.vida = 100
        self.vel_x = 0
        self.vel_y = 0
        self.velocidade = 10
        self.aceleracao = Vetor(0, 10)
            
        self.intervalo_lancamento_pedra = 4
        self.pode_lancar = True
        self.tempo_mudar_direcao = 0
        self.vivo = True
        self.dano = self.definir_dano(nivel_dificuldade)
        self.campo_de_visao = 40 * TAMANHO_QUADRADO
            
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

    def checar_atingido(self, projeteis):
        for projetil in projeteis:
            if projetil.retangulo.colidiu_com(self.retangulo):
                self.vida -= projetil.dano
                projetil.ativo = False
                if self.vida <= 0: self.vida = 0

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
        
    