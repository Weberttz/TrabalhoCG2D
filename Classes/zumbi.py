from settings import TAMANHO_QUADRADO, TAMANHO_ZUMBI, random
from Classes.humanoide import Humanoide

class Zumbi(Humanoide):
    def __init__(self, plataformas, pos, equipamentos, cor, nivel_dificuldade):
        super().__init__(plataformas, [], equipamentos, pos, cor, TAMANHO_ZUMBI)
        self.vertices = []
        self.tempo_mudar_direcao = 0
        self.vivo = True
        self.dano = self.definir_dano(nivel_dificuldade)
        self.campo_visao = 10 * TAMANHO_QUADRADO # enxerga 10 blocos
        self.bateu_cabeca = False

    def atualizar(self, projeteis):
        self.aplicar_gravidade()
        self.atualizar_vertices()
        self.lidar_com_colisoes()
        self.movimentar()
        self.atualizar_vertices_equipamento()
        self.checar_atingido(projeteis)
        self.morrer()

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

    def lidar_com_colisoes(self):
        for plataforma in self.plataformas:
            if plataforma.retangulo.colidiu_com(self.retangulo):
                self.vel_x = 0
                self.bateu_cabeca = True

        return super().lidar_com_colisoes()
    
    def movimentar(self):
        self.inimigo = self.inimigos[0]
        # Diminui o contador e muda de direção aleatoriamente ao zerar
        self.tempo_mudar_direcao -= 1

         # se bateu cabeça, troca de direção e anda por um bom tempo até querer voltar ao normal
        if self.bateu_cabeca: 
            self.vel_x = -self.vel_x
            self.olhando *= -1
            self.bateu_cabeca = False
            self.tempo_mudar_direcao = random.randint(30, 60) # dobro do tempo max normalmente
            return
        
        if self.tempo_mudar_direcao <= 0:
            esta_no_campo_de_visao = (abs(self.inimigo.pos.x - self.pos.x) < self.campo_visao)

            if esta_no_campo_de_visao:
                if self.inimigo.pos.x != self.pos.x:
                    sinal = ((self.inimigo.pos.x - self.pos.x) / abs(self.inimigo.pos.x - self.pos.x))
                    self.vel_x = 3 * sinal
                    self.olhando = -1 * sinal
                else:
                    self.vel_x = 0
            else: 
                self.vel_x = random.choice([-1, 0, 1])

            self.tempo_mudar_direcao = random.randint(30, 60)  # Quadros (Frames)
