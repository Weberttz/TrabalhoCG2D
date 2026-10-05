import pygame 
import Biblioteca.transformacoes as transformacoes
from Classes.humanoide import Humanoide
from settings import Vetor, Retangulo

class Jogador(Humanoide):
    def __init__(self, pos, plataformas, inimigos, coletaveis, equipamentos, cor):
        super().__init__(plataformas, inimigos, equipamentos, pos, cor)
        self.tempo = pygame.time.get_ticks()
        self.pontuacao = 0
        self.coletaveis_missao = 0
        self.olhando = 1
        self.coletaveis = coletaveis
        self.quantidade_coletada = 0
        self.invulneravel = False
        self.tempo_invulnerabilidade = 1.0  # 1 seg
        self.momento_ultimo_dano = 0
        self.forca_afastamento = 20
        self.atrito_afastamento = 0.85
        self.vel_afastamento = 0
        self.tempo_teleport = 2.0
        self.momento_ultimo_teleport = 100
        self.teleport_colidiu = None
        self.momento_entrada_teleport = None 
        self.quantidade_inimigos_anterior = len(inimigos)

    def resetar(self, pos_inicial):
        self.pos = pos_inicial.copy()
        self.vel_x = 0
        self.vel_y = 0
        self.aceleracao = Vetor(0, 10) 
        self.no_chao = False
        # self.vida = 100
        self.retangulo = Retangulo(self.pos.x, self.pos.y - self.tamanho,
                                self.tamanho, self.tamanho)
        self.atualizar_vertices()

    def atualizar(self):
        '''Atualiza os atributos do jogador.'''
        self.lidar_com_inputs()
        self.aplicar_gravidade()
        self.atualizar_vertices()
        self.lidar_com_colisoes()
        self.atualizar_vertices_equipamento()
        self.atirar()
        self.atualizar_invulnerabilidade()
        self.contabilizar_pontuacao()

    def get_direcao_tiro(self):
        '''Determina a direção do tiro.'''
        keys = pygame.key.get_pressed()

        x = 0
        if keys[pygame.K_RIGHT]: x += 1
        if keys[pygame.K_LEFT]:  x -= 1

        y = 0
        if keys[pygame.K_UP] and x == 0:   y -= 1    # cima
        # if keys[pygame.K_DOWN] and not self.no_chao: y += 1  # baixo só no ar

        if x == 0 and y == 0:
            x = self.olhando              # parado: atira para onde olha

        direcao = Vetor(x, y)
        return direcao.normalizar()

    def atirar(self):
        '''Recebe comandos de teclado para atirar projéteis.
           \nArma acionada pela tecla : Z  
        '''
        pos = Vetor(self.pos.x + self.tamanho // 2,
                            self.pos.y - self.tamanho // 2 - self.equipamento.altura)

        tempo = pygame.time.get_ticks()
        if tempo - self.equipamento.tempo >= self.equipamento.intervalo_tiro:
            self.equipamento.tempo = tempo
            self.equipamento.pode_atirar = True

        if pygame.key.get_pressed()[pygame.K_z]:
            self.equipamento.atacar(self.get_direcao_tiro(), pos)

    def lidar_com_inputs(self):
        '''Recebe comandos de teclado para mover o jogador. 
            \nLEFT - volta para o começo do mapa
            \nRIGHT - segue para o fim do mapa
            \nSPACE - pula
        '''
        keys = pygame.key.get_pressed()

        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x += -self.velocidade
            self.olhando = -1
    
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.velocidade
            self.olhando = 1

        if keys[pygame.K_SPACE] and self.no_chao:
            self.aceleracao.y = self.forca_pulo
            self.no_chao = False

        self.vel_x += self.vel_afastamento
        self.vel_afastamento *= self.atrito_afastamento

        print(f" vel_x = {self.vel_x}")

    def lidar_com_colisoes(self):
        self.colidir_com_coletavel()
        self.colidir_com_inimigo()
        self.colidir_com_teleport()
        return super().lidar_com_colisoes()

    def colidir_com_teleport(self):
        '''Detecta se o jogador está na área de teletransporte e teleporta.'''
        teleports = [p for p in self.plataformas if p.tipo == "teleport"]

        # encontrar teleport atual
        atual = None
        for t in teleports:
            if self.retangulo.colidiu_com(t.retangulo):
                atual = t
                break

        # se saiu do teleport, então destrava
        if atual is None:
            self.teleport_colidiu = None
            self.momento_entrada_teleport = None
            return
        
        agora = pygame.time.get_ticks()

        # começou a encostar: inicia a contagem
        if atual is not self.teleport_colidiu:
            self.teleport_colidiu = atual
            self.momento_entrada_teleport = agora
            return
        
        # se não passou o tempo mínimo de 4 segundos
        if agora - self.momento_entrada_teleport < self.tempo_teleport * 1000:
            return

        # encontrar o teleport mais próximo
        alvo = None
        menor_distancia = float("inf")
        for t in teleports:
            if t is atual:
                continue
            distancia = abs(atual.x0 - t.x0) + abs(atual.y0 - t.y0)
            if distancia < menor_distancia:
                menor_distancia = distancia
                alvo = t

        if alvo is None:
            return

        pos_atual = [[self.pos.x], [self.pos.y], [1]]
        transladacao_origem = transformacoes.translacao(-self.pos.x, -self.pos.y)
        transladacao_destino = transformacoes.translacao(alvo.x0, alvo.y1)
        matriz_composta = transformacoes.produto_matriz(transladacao_origem, transladacao_destino)
        pos_final = transformacoes.produto_matriz(matriz_composta, pos_atual)
        self.pos = Vetor(pos_final[0], pos_final[1])

        self.teleport_colidiu = None
        self.momento_entrada_teleport = None
    
    def colidir_com_coletavel(self):
        '''Trata colisão com coletáveis'''
        for coletavel in self.coletaveis:
            if self.retangulo.colidiu_com(coletavel.retangulo) and coletavel.ativo:
                if coletavel.tipo == "tapioca":
                    self.vida+= 30 
                if coletavel.tipo == "municao":
                    self.equipamento.municao+=1

                if coletavel.tipo == "especial":
                    self.pontuacao += 100
                    self.coletaveis_missao+=1

                self.quantidade_coletada += 1
                coletavel.ativo = False   

        if self.vida < 100: self.vida = 100

    def contabilizar_pontuacao(self):
        qnt_inimigos = len(self.inimigos)

        diferenca = self.quantidade_inimigos_anterior - qnt_inimigos

        if qnt_inimigos < self.quantidade_inimigos_anterior:
            self.quantidade_inimigos_anterior = qnt_inimigos
            self.pontuacao+= diferenca * 50
    
    def colidir_com_inimigo(self):
        '''Trata colisão com inimigos.
        \n Ordem dos acontecimentos da reação - o jogador:
        \n - Perde vida;
        \n - É afastado do inimigo; 
        \n - Torna-se temporariamente invulnerável. ''' 
        for inimigo in self.inimigos:
            if self.retangulo.colidiu_com(inimigo.retangulo) and not self.invulneravel:
                print(f'Dano inimigo: {inimigo.dano}')
                self.vida -= inimigo.dano
                self.afastar_do_inimigo(inimigo)
                self.invulneravel = True
                self.momento_ultimo_dano = pygame.time.get_ticks() 

    def atualizar_invulnerabilidade(self):
        '''Verifica se já passou o tempo de invulnerabilidade:
        \n - se sim, torna vulnerável outra vez
        \n - se não, permanece invulnerável (não perde vida em colisões com inimigos)
        '''
        if self.invulneravel:
            if (pygame.time.get_ticks() - self.momento_ultimo_dano) >= self.tempo_invulnerabilidade * 1000:
                self.invulneravel = False
                self.vel_afastamento = 0

    def afastar_do_inimigo(self, inimigo):
        # primeiro afasta e depois torna invulneravel
        # pq assim afasta so uma vez por segundo tbm
        # se colidir pela esquerda, empurra pra esquerda
        if self.pos.x < inimigo.pos.x:
            direcao = -1
        else:
            direcao = 1
        self.vel_afastamento = direcao * self.forca_afastamento