from settings import ( 
    LARGURA, 
    POS_INICIO, 
    VEL_ANIMACAO, 
    TAMANHO_QUADRADO, 
    Vetor
)

def atualizar_jogador(jogo):
    verificar_morte_jogador(jogo)
    verificar_passou_de_fase(jogo)
    verificar_voltou_fase(jogo)
    jogo.jogador.atualizar()

def atualizar_animacao(jogo, dt):
    jogo.tempo_animacao += dt
    jogo.avancar_frame = jogo.tempo_animacao >= VEL_ANIMACAO
    if jogo.avancar_frame:
        jogo.tempo_animacao = 0.0

def atualizar_entidades(jogo, dt):
    remover_entidades_inativas(jogo)
    atualizar_visiveis(jogo)         
    atualizar_coletaveis(jogo)
    atualizar_projeteis(jogo, dt)
    atualizar_zumbis(jogo)



    

def verificar_morte_jogador(jogo):
    j = jogo.jogador
    if j.vida <= 0 or j.pos.y > jogo.altura_mapa:
        j.resetar(POS_INICIO)
        j.vida = 100

def verificar_passou_de_fase(jogo):
    j = jogo.jogador
    if j.pos.x > jogo.largura_mapa:
        j.resetar(POS_INICIO)
        jogo.gerenciadorFases.avancar()

        if jogo.gerenciadorFases.terminou():
            jogo.run_finalizada = True
            return

        jogo.carregar_fase(jogo.gerenciadorFases.caminho_fase_atual())

def verificar_voltou_fase(jogo):
    j = jogo.jogador
    if j.pos.x >= 0:
        return

    if jogo.gerenciadorFases.fase_atual == 0:
        j.pos.x = 0                   
        j.retangulo.x = 0
        return

    jogo.gerenciadorFases.voltar()
    j.resetar(Vetor(jogo.gerenciadorFases.largura_fase_atual() - TAMANHO_QUADRADO, 690))
    jogo.voltando = True
    jogo.carregar_fase(jogo.gerenciadorFases.caminho_fase_atual())



def remover_entidades_inativas(jogo):
    jogo.zumbis[:] = [z for z in jogo.zumbis if z.vivo]

def atualizar_visiveis(jogo):
    dx, _ = jogo.camera.retangulo.topleft
    jogo.zumbis_visiveis = [
        z for z in jogo.zumbis
        if -dx - z.tamanho <= z.pos.x <= -dx + LARGURA
    ]
    jogo.coletaveis_visiveis = [
        c for c in jogo.coletaveis
        if -dx - c.tamanho <= c.pos.x <= -dx + LARGURA
    ]

def atualizar_coletaveis(jogo):
    jogo.coletaveis[:] = [c for c in jogo.coletaveis if c.ativo]

def atualizar_projeteis(jogo, dt):
    projeteis = jogo.jogador.equipamento.projetils
    projeteis[:] = [p for p in projeteis if p.ativo]
    for projetil in projeteis:
        projetil.atualizar(dt, jogo.plataformas)  

def atualizar_zumbis(jogo):
    projeteis = jogo.jogador.equipamento.projetils
    for zumbi in jogo.zumbis_visiveis:
        zumbi.atualizar(projeteis)
        if jogo.avancar_frame:
            zumbi.animar(jogo.anim_idle, jogo.anim_esquerda, jogo.anim_direita)