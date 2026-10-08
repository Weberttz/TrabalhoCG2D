import math

def set_pixel(superficie, x, y, cor, clip_atual = None):
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((int(x), int(y)), cor)

def preencher_retangulo(superficie, retangulo, cor ):
    xmin, ymin, xmax, ymax = retangulo

    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            superficie.set_at((x, y), cor)

def draw_line(superficie, pontos, cor):
    for (x, y) in pontos:
        set_pixel(superficie, x, y, cor)

def draw_polygonon(superficie, vertices, color, clip_atual = None):
    n = len(vertices)
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i+1) % n]
        linha_bresenham(superficie, x0, y0, x1, y1, color, clip_atual)
  
def linha_bresenham(superficie, x0, y0, x1, y1, cor, clip_atual = None):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
        set_pixel(superficie, x0, y0, cor, clip_atual)

def scanline_fill(superficie, pontos, cor_preenchimento, clip_atual = None):
    ys = [p[1] for p in pontos] # Lista só de Y
    y_min = min(ys) 
    y_max = max(ys)

    n = len(pontos)

    for y in range(int(y_min), int(y_max)): # do mínimo ao máximo de y, movimento vertical
        interseccoes_x = []
        for i in range(n): # pegar cada ponto do vetor de pontos
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i+1) % n]

            if y0 == y1: continue # se estiverem alinhados na horizontal, não fazer nada

            if y0 >= y1: # se a orientação estiver errada, trocar os valores
                x0, y0, x1, y1 = x1, y1, x0, y0

            if y <= y0 or y >= y1: continue # se estiver fora da área, não fazer nada

            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0) # fórmula da interpolação
            interseccoes_x.append(x)

        interseccoes_x.sort()

        for i in range(0, len(interseccoes_x), 2): # pegar os pontos dois a dois
            if i+1 >= len(interseccoes_x): break

            x_inicio = int(round(interseccoes_x[i]) + 1) # x inicio e x fim 
            x_fim =  int(round(interseccoes_x[i+1]))

            for x in range(x_inicio, x_fim):
                set_pixel(superficie, x, y, cor_preenchimento, clip_atual)

def flood_fill_iterativo(superficie, x, y, cor_preenchimento, cor_borda):
    largura = superficie.get_width()
    altura = superficie.get_height()

    pilha = [(x, y)]

    while pilha:
        x, y = pilha.pop()

        if not (0 <= x < largura and 0 <= y < altura):
            continue

        cor_atual = superficie.get_at((x, y))
        if cor_atual == cor_borda or cor_atual == cor_preenchimento:
            continue

        set_pixel(superficie, x, y, cor_preenchimento)

        pilha.append((x + 1, y))
        pilha.append((x - 1, y))
        pilha.append((x, y + 1))
        pilha.append((x, y - 1))


def desenhar_aabb(superficie, aabb, cor):

    x1, y1, x2, y2 = aabb

    pontos = [
        (x1, y1),
        (x2, y1),
        (x2, y2),
        (x1, y2)
    ]

    draw_polygonon(superficie, pontos, cor)

def pontos_circulo(cx, cy, raio):
    pontos = []
    x, y = 0, raio
    d = 1 - raio                     # para decisão

    while x <= y:
        # simetria de 8 vias
        for px, py in ((x, y), (y, x), (-x, y), (-y, x),
                       (x, -y), (y, -x), (-x, -y), (-y, -x)):
            pontos.append((cx + px, cy + py))

        x += 1
        if d < 0:                  
            d += 2 * x + 1
        else:                       
            y -= 1
            d += 2 * (x - y) + 1

    return pontos

def linhas_circulo_preenchido(cx, cy, raio):
    linhas = []
    for dy in range(-raio, raio + 1):
        dx = int(math.sqrt(raio * raio - dy * dy))
        linhas.append((cy + dy, cx - dx, cx + dx))
    return linhas

def desenhar_circulo(superficie, centro, raio, cor, preenchido=False):
    largura, altura = superficie.get_size()
    cx, cy = int(centro[0]), int(centro[1])
    raio = int(raio)

    if preenchido:
        for y, x1, x2 in linhas_circulo_preenchido(cx, cy, raio):
            if 0 <= y < altura:
                for x in range(max(x1, 0), min(x2, largura - 1) + 1):
                    set_pixel(superficie, x, y, cor)
    else:
        for x, y in pontos_circulo(cx, cy, raio):
            if 0 <= x < largura and 0 <= y < altura:
                set_pixel(superficie, x, y, cor)


def bresenham_circulo(superficie, xc, yc, r, cor):
    x = 0
    y = r
    d = 1 - r  # variável de decisão clássica

    plotar8(superficie, xc, yc, x, y, cor)

    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        plotar8(superficie, xc, yc, x, y, cor)


def plotar8(superficie, xc, yc, x, y, cor):
    set_pixel(superficie, xc + x, yc + y, cor)
    set_pixel(superficie, xc - x, yc + y, cor)
    set_pixel(superficie, xc + x, yc - y, cor)
    set_pixel(superficie, xc - x, yc - y, cor)
    set_pixel(superficie, xc + y, yc + x, cor)
    set_pixel(superficie, xc - y, yc + x, cor)
    set_pixel(superficie, xc + y, yc - x, cor)
    set_pixel(superficie, xc - y, yc - x, cor)

def plotar4(superficie, xc, yc, x, y, cor):
    set_pixel(superficie, xc + x, yc + y, cor)
    set_pixel(superficie, xc - x, yc + y, cor)
    set_pixel(superficie, xc + x, yc - y, cor)
    set_pixel(superficie, xc - x, yc - y, cor)

def linha_h(superficie, x1, x2, y, cor):
    for x in range(x1, x2 + 1):
        set_pixel(superficie, x, y, cor)

def preencher4(superficie, xc, yc, x, y, cor): # passa a linha para fazer setpixel em cada ponto da linha
    linha_h(superficie, xc - x, xc + x, yc + y, cor)
    if y != 0:  # evita redesenhar a linha central
        linha_h(superficie, xc - x, xc + x, yc - y, cor)

def desenhar_elipse(superficie, xc, yc, rx, ry, cor, preenchida = False):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    d1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    while dx < dy:
        if not preenchida:
            plotar4(superficie, xc, yc, x, y, cor)
        else:
            preencher4(superficie, xc, yc, x, y, cor)
        x += 1
        dx += 2 * ry2

        if d1 < 0:
            d1 += dx + ry2
        else:
            y -= 1
            dy -= 2 * rx2
            d1 += dx - dy + ry2

    d2 = (ry2 * ((x + 0.5) ** 2)) + (rx2 * ((y - 1) ** 2)) - (rx2 * ry2)

    while y >= 0:
        if not preenchida:
            plotar4(superficie, xc, yc, x, y, cor)
        else:
            preencher4(superficie, xc, yc, x, y, cor)

        y -= 1
        dy -= 2 * rx2

        if d2 > 0:
            d2 += rx2 - dy
        else:
            x += 1
            dx += 2 * ry2
            d2 += dx - dy + rx2
    

# Clipping Cohen-Sutherland
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8


def codigo_regiao(x, y, xmin, ymin, xmax, ymax):
    '''Recebe um ponto e determina a localização dele em relação a uma janela
        dada por dois pontos (máximo e mínimo).'''
    codigo = INSIDE
    if x < xmin:
        codigo |= LEFT

    elif x > xmax:
        codigo |= RIGHT

    if y < ymin:
        codigo |= TOP

    elif y > ymax:
        codigo |= BOTTOM

    return codigo

def cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    ''' Recebe dois pares de pontos que determinam uma reta e uma janela 
    (com seus pontos máximo e mínimo)
    \nReturn se a reta tem alguma parte visivel na janela e as coordenadas 
    de intersecção com a ela.
    '''
    c0 = codigo_regiao(x0, y0, xmin, ymin, xmax, ymax)

    c1 = codigo_regiao(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if not (c0 | c1):
            return (True, x0, y0, x1, y1)
        
        if c0 & c1:
            return (False, 0, 0, 0, 0)

        c_out = c0 if c0 else c1

        if c_out & TOP:
            x = ( x0 + (x1 - x0) * (ymin - y0) / (y1 - y0))
            y = ymin

        elif c_out & BOTTOM:
            x = (x0 + (x1 - x0) * (ymax - y0) / (y1 - y0))
            y = ymax

        elif c_out & RIGHT:

            y = ( y0 + (y1 - y0) * (xmax - x0) / (x1 - x0))
            x = xmax

        else:
            y = (y0 + (y1 - y0) * (xmin - x0) / (x1 - x0))
            x = xmin

        if c_out == c0:
            x0 = x
            y0 = y
            c0 = codigo_regiao(x0, y0, xmin, ymin, xmax, ymax)

        else:
            x1 = x
            y1 = y
            c1 = codigo_regiao(x1, y1, xmin, ymin, xmax, ymax)

def retangulo_para_poligono(x, y, largura, altura):
    return [
        (x, y),
        (x + largura, y),
        (x + largura, y + altura),
        (x, y + altura)
    ]

def scanline_texture(superficie, pontos, uvs, textura, cor_efeito=None):
    tex_w = textura.get_width()
    tex_h = textura.get_height()

    n = len(pontos)
    ys = [p[1] for p in pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    for y in range(y_min, y_max):
        intersecoes = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]
            u0, v0 = uvs[i]
            u1, v1 = uvs[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                u0, v0, u1, v1 = u1, v1, u0, v0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)

            x = x0 + t * (x1 - x0)
            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)

            intersecoes.append((x, u, v))

        intersecoes.sort(key=lambda item: item[0])

        for i in range(0, len(intersecoes), 2):
            if i + 1 >= len(intersecoes):
                continue

            x_ini, u_ini, v_ini = intersecoes[i]
            x_fim, u_fim, v_fim = intersecoes[i + 1]

            if x_fim == x_ini:
                continue

            for x in range(int(x_ini), int(x_fim) + 1):

                t = (x - x_ini) / (x_fim - x_ini)

                u = u_ini + t * (u_fim - u_ini)
                v = v_ini + t * (v_fim - v_ini)

                tx = int(u * (tex_w - 1))
                ty = int(v * (tex_h - 1))

                if not (0 <= tx < tex_w and 0 <= ty < tex_h):
                    continue

                cor_original = textura.get_at((tx, ty))
                a = cor_original.a

                # pixel transparente da sprite
                if a == 0:
                    continue

                if not (
                    0 <= x < superficie.get_width()
                    and 0 <= y < superficie.get_height()
                ):
                    continue

                if cor_efeito is not None:
                    r, g, b = cor_efeito
                else:
                    r = cor_original.r
                    g = cor_original.g
                    b = cor_original.b

                # mantém o alpha original da sprite
                if a < 255:
                    fundo = superficie.get_at((x, y))
                    fator = a / 255

                    cor = (
                        int(r * fator + fundo.r * (1 - fator)),
                        int(g * fator + fundo.g * (1 - fator)),
                        int(b * fator + fundo.b * (1 - fator)),
                    )

                else:
                    cor = (r, g, b)

                set_pixel(superficie, x, y, cor)

def interpola_cor(c1, c2, t):
    r = int(c1[0] + (c2[0]-c1[0])*t)
    g = int(c1[1] + (c2[1]-c1[1])*t)
    b = int(c1[2] + (c2[2]-c1[2])*t)

    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    
    return (r, g, b)

def scanline_fill_gradiente(superficie, pontos, cores):
    ys = [p[1] for p in pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(pontos)

    for y in range(y_min, y_max):
        intersecoes = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            c0 = cores[i]
            c1 = cores[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                c0, c1 = c1, c0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)
            cor_y = interpola_cor(c0, c1, t)

            intersecoes.append((x, cor_y))

        intersecoes.sort(key=lambda i: i[0])

        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                x_ini, cor_ini = intersecoes[i]
                x_fim, cor_fim = intersecoes[i + 1]

                if x_fim == x_ini:
                    continue

                for x in range(int(x_ini), int(x_fim) + 1):
                    t = (x - x_ini) / (x_fim - x_ini)
                    cor = interpola_cor(cor_ini, cor_fim, t)
                    set_pixel(superficie, x, y, cor)