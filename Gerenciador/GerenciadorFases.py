from Gerenciador import Inicializador

class GerenciadorFases:
    def __init__(self, fases, TAMANHO_QUADRADO):
        self.fases = fases
        self.fase_atual = 0
        self.max_fases = len(fases)
        self.larguras = [len(Inicializador.carregar_mapa(fase)[0]) * TAMANHO_QUADRADO 
                        for fase in self.fases] 
        self.alturas =  [len(Inicializador.carregar_mapa(fase)) * TAMANHO_QUADRADO 
                        for fase in self.fases]  

    def definir_dificuldade(self, nivel_dificuldade):
        self.dificuldade = nivel_dificuldade

    def caminho_fase_atual(self):
        return self.fases[self.fase_atual]

    def largura_fase_atual(self):
        return self.larguras[self.fase_atual]

    def altura_fase_atual(self):
        return self.alturas[self.fase_atual]
    
    def avancar(self):
        if(self.fase_atual < len(self.fases)):
            self.fase_atual += 1

    def voltar(self):
        if self.fase_atual > 0 :
            self.fase_atual -= 1

    # conclusão provisória
    def verificar_conclusao(self, jogo):
        '''Verifica se:
        \n - o jogador morreu (game_over);
        \n - o chefe morreu (win) '''
        self.win(jogo)
        self.game_over(jogo)

    def win(self,jogo):
        if jogo.chefe != None: 
            if jogo.chefe.vida == 0:
                jogo.estado_jogo = "Win"

    def game_over(self,jogo):
        if jogo.jogador.vida == 0 or jogo.jogador.pos.y > jogo.altura_mapa:
            jogo.estado_jogo = "Game over"

    def terminou(self):
        return self.fase_atual >= len(self.fases)

    def reiniciar(self):
        self.fase_atual = 0
