import random
from Classes.humanoide import Humanoide
from settings import TAMANHO_QUADRADO

class Cachorro(Humanoide):
    def __init__(self, plataformas, pos, equipamentos, cor, nivel_dificuldade):
        super().__init__(plataformas, [], equipamentos, pos, cor)
        self.vertices = []
        self.tempo_mudar_direcao = 0
        self.vivo = True
        self.dano = self.definir_dano(nivel_dificuldade)
        self.campo_de_visao = 20 * TAMANHO_QUADRADO
        self.bateu_cabeca = False

    def atualizar(self):
        self.aplicar_gravidade()
        self.movimentar()
        self.lidar_com_colisoes()
        self.atualizar_vertices()

    def definir_dano(self,nivel_dificuldade):
        '''Define o dano do inimigo pelo nível de dificuldade escolhido pelo jogador.'''
        if nivel_dificuldade == 'facil':
            return 10
        elif nivel_dificuldade == 'medio':
            return 20
        elif nivel_dificuldade == 'dificil':
            return 40

    def lidar_com_colisoes(self):
        for plataforma in self.plataformas:
            if plataforma.retangulo.colidiu_com(self.retangulo):
                self.vel_x = 0
                if plataforma.tipo != "block":
                    self.bateu_cabeca = True
        return super().lidar_com_colisoes()
    
    def movimentar(self):
        self.inimigo = self.inimigos[0]
        # Move o zumbi baseado na direção atual
        self.retangulo.x += self.vel_x * self.velocidade

        # Diminui o contador e muda de direção aleatoriamente ao zerar
        self.tempo_mudar_direcao -= 1
        if self.tempo_mudar_direcao <= 0:
            esta_no_campo_de_visao = (abs(self.inimigo.pos.x - self.pos.x) < self.campo_de_visao)

            if esta_no_campo_de_visao:
                if self.inimigo.pos.x != self.pos.x:
                    self.vel_x = ((self.inimigo.pos.x - self.pos.x) / abs(self.inimigo.pos.x - self.pos.x))
                    self.vel_x *= 2
                else:
                    self.vel_x = 0
            else: 
                self.vel_x = random.choice([-1, 0, 1])

            self.tempo_mudar_direcao = random.randint(30, 60)  # Quadros (Frames)

            # se bateu cabeça, troca de direção e anda por um bom tempo até querer voltar ao normal
            if self.bateu_cabeca: 
                self.vel_x = -self.vel_x
                self.bateu_cabeca = False
                self.tempo_mudar_direcao = 120 # dobro do tempo max normalmente
