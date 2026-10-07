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
        if not self.inimigos:
            return

        self.inimigo = self.inimigos[0]

        # Distância horizontal até o inimigo
        distancia_x = self.inimigo.pos.x - self.pos.x

        esta_no_campo_de_visao = abs(distancia_x) < self.campo_visao

        # Se bateu em uma parede, vai inverter imediatamente
        if self.bateu_cabeca:
            if self.vel_x != 0:
                self.vel_x *= -1
                self.olhando *= -1
            else:
                self.vel_x = random.choice([-1, 1])
                self.olhando = self.vel_x

            self.bateu_cabeca = False
            self.tempo_mudar_direcao = random.randint(30, 60)
            return

        # Se viu o jogador, persegue continuamente
        if esta_no_campo_de_visao:

            if distancia_x > 0:
                self.vel_x = 3
                self.olhando = 1

            elif distancia_x < 0:
                self.vel_x = -3
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
