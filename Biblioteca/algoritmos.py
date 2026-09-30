import math
from Biblioteca import transformacoes

def set_pixel(superficie, x, y, cor):
    superficie.set_at((int(x), int(y)), cor)

def draw_line(superficie, pontos, cor):
    for (x, y) in pontos:
        set_pixel(superficie, x, y, cor)

def draw_polygonon(superficie, vertices, color):
    n = len(vertices)
    superficie.lock()
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i+1) % n]
        linha_bresenham(superficie, x0, y0, x1, y1, color)
    superficie.unlock()
  
def linha_bresenham(superficie, x0, y0, x1, y1, cor):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    set_pixel = superficie.set_at

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
        set_pixel((int(x0), int(y0)), cor)

def scanline_fill(superficie, pontos, cor_preenchimento):
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

            set_pixel = superficie.set_at
            for x in range(x_inicio, x_fim):
                set_pixel((x, y), cor_preenchimento)

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

    set_pixel = superficie.set_at
    if preenchido:
        for y, x1, x2 in linhas_circulo_preenchido(cx, cy, raio):
            if 0 <= y < altura:
                for x in range(max(x1, 0), min(x2, largura - 1) + 1):
                    set_pixel((x, y), cor)
    else:
        for x, y in pontos_circulo(cx, cy, raio):
            if 0 <= x < largura and 0 <= y < altura:
                set_pixel((x, y), cor)


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


def desenhar_elipse(superficie, xc, yc, rx, ry, cor):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    d1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    while dx < dy:
        plotar4(superficie, xc, yc, x, y, cor)
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
        plotar4(superficie, xc, yc, x, y, cor)

        y -= 1
        dy -= 2 * rx2

        if d2 > 0:
            d2 += rx2 - dy
        else:
            x += 1
            dx += 2 * ry2
            d2 += dx - dy + rx2

def matriz_janela_viewport(janela, viewport):

    Wxmin, Wymin, Wxmax, Wymax = janela
    Vxmin, Vymin, Vxmax, Vymax = viewport

    sx = ((Vxmax - Vxmin)
        / (Wxmax - Wxmin))

    sy = ((Vymax - Vymin)
        / (Wymax - Wymin))

    M = transformacoes.identidade()
    # Janela -> Origem
    M = transformacoes.produto_matriz(
        transformacoes.translacao(-Wxmin,-Wymin),
        M)

    # Escala
    M = transformacoes.produto_matriz(
        transformacoes.escala(sx, sy),
        M)

    # Origem -> viewport

    M = transformacoes.produto_matriz(
        transformacoes.translacao(Vxmin,Vymin),
        M)

    return M

def retangulo_para_poligono(
    x,
    y,
    largura,
    altura
):

    return [
        (x, y),
        (x + largura, y),
        (x + largura, y + altura),
        (x, y + altura)
    ]
