from settings import (
    LARGURA,
    POS_INICIO,
    VEL_ANIMACAO
)


def atualizar_jogador(self):
    self.verificar_morte_jogador()
    self.verificar_passou_de_fase()
    self.jogador.atualizar()

def atualizar_entidades(self, dt):
    self.remover_entidades_inativas()
    self.atualizar_coletaveis()
    self.atualizar_projeteis(dt)
    self.atualizar_zumbis()
    self.atualizar_visiveis()

def verificar_morte_jogador(self):
    j = self.jogador
    if j.vida <= 0 or j.pos.y > self.altura_mapa:
        j.pos = POS_INICIO.copy()
        j.vida = 100

def verificar_passou_de_fase(self):
    j = self.jogador
    if j.pos.x > self.largura_mapa:
        j.pos = POS_INICIO.copy()
        self.fase_atual+=1

        if self.fase_atual == self.max_fases:
            self.fase_atual -= 1
            self.run_finalizada = True
            return

        self.carregar_fase(self.fases[self.fase_atual])

def atualizar_visiveis(self):
    dx, _ = self.camera.camera.topleft
    self.zumbis_visiveis = [
        z for z in self.zumbis
        if -dx - z.tamanho <= z.pos.x <= -dx + LARGURA
    ]
    self.coletaveis_visiveis = [
        c for c in self.coletaveis
        if -dx - c.tamanho <= c.pos.x <= -dx + LARGURA
    ]

def atualizar_coletaveis(self):
    coletaveis = self.coletaveis
    coletaveis[:] = [c for c in coletaveis if c.ativo]

def atualizar_projeteis(self, dt):
    projeteis = self.jogador.equipamento.projetils
    projeteis[:] = [p for p in projeteis if p.ativo]   # remove os que não estão ativos
    for projetil in projeteis:
        projetil.atualizar(dt)

def atualizar_animacao(self, dt):
    self.tempo_animacao += dt
    self.avancar_frame = self.tempo_animacao >= VEL_ANIMACAO
    if self.avancar_frame:
        self.tempo_animacao = 0.0

def atualizar_zumbis(self):
    projeteis = self.jogador.equipamento.projetils
    for zumbi in self.zumbis_visiveis:
        zumbi.atualizar(projeteis)
        if self.avancar_frame:
            zumbi.animar(self.anim_idle, self.anim_esquerda, self.anim_direita)

