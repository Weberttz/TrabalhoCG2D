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
    atualizar_cachorros(jogo)
    atualizar_pombos(jogo)

def verificar_morte_jogador(jogo):
    j = jogo.jogador
    if j.vida <= 0 or j.pos.y > jogo.altura_mapa:
        j.resetar(POS_INICIO)
        j.vida = 100

def verificar_passou_de_fase(jogo):
    j = jogo.jogador
    x_inicial = 10
    if j.pos.x > jogo.largura_mapa:
        j.resetar(Vetor(x_inicial, j.pos.y - j.tamanho))
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
    """Altera a lista em memória, sem duplicar"""
    jogo.zumbis[:] = [z for z in jogo.zumbis if z.vivo] # remove os zumbis mortos da lista
    jogo.pombos[:] = [p for p in jogo.pombos if p.vivo] #  remove os cachorros mortos
    jogador = jogo.jogador
    jogador.inimigos[:] = [i for i in jogador.inimigos if i.vivo] # remove da 'visão' do jogador todos os inimigos

def atualizar_visiveis(jogo):
    """Atualiza listas colocando apenas os inimigos que estão na tela"""
    dx, _ = jogo.camera.retangulo.topleft
    jogo.zumbis_visiveis = [
        z for z in jogo.zumbis
        if -dx - z.tamanho <= z.pos.x <= -dx + LARGURA
    ]
    jogo.coletaveis_visiveis = [
        c for c in jogo.coletaveis
        if -dx - c.tamanho <= c.pos.x <= -dx + LARGURA
    ]
    jogo.cachorros_visiveis = [
        c for c in jogo.cachorros
        if -dx - c.tamanho <= c.pos.x <= -dx + LARGURA
    ]
    jogo.pombos_visiveis = [
        p for p in jogo.pombos
        if -dx - p.tamanho <= p.pos.x <= -dx + LARGURA
    ]
    jogo.portais_visiveis = [
        p for p in jogo.portais
        if -dx - p.largura <= p.x0 <= -dx + LARGURA
    ]

def atualizar_coletaveis(jogo):
    """Remove os coletáveis que já foram pegos"""
    jogo.coletaveis[:] = [c for c in jogo.coletaveis if c.ativo]

def atualizar_projeteis(jogo, dt):
    """Atualiza o estado do projétil e remove os que estão inativos da lista"""
    projeteis = jogo.jogador.equipamento.projeteis
    projeteis[:] = [p for p in projeteis if p.ativo]
    for projetil in projeteis:
        projetil.atualizar(dt, jogo.plataformas)  

    colisores = [p for p in jogo.plataformas]
    colisores.append(jogo.jogador)
    for pombo in jogo.pombos:
        pedras = pombo.pedras
        pedras[:] = [p for p in pedras if p.ativo]
        for pedra in pedras:
            pedra.atualizar(dt, colisores)

def atualizar_pombos(jogo):
    projeteis = jogo.jogador.equipamento.projeteis
    for pombo in jogo.pombos_visiveis:
        pombo.atualizar(projeteis)

def atualizar_zumbis(jogo):
    projeteis = jogo.jogador.equipamento.projeteis
    for zumbi in jogo.zumbis_visiveis:
        zumbi.atualizar(projeteis)
        if jogo.avancar_frame:
            zumbi.animar(jogo.anim_zumbi_idle, jogo.anim_zumbi_esquerda, jogo.anim_zumbi_direita)

def atualizar_cachorros(jogo):
    for cachorro in jogo.cachorros_visiveis:
        cachorro.atualizar()
        if jogo.avancar_frame:
            cachorro.animar(jogo.anim_cachorro_idle, jogo.anim_cachorro_esquerda, jogo.anim_cachorro_direita)