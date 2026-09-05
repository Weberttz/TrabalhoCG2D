def set_pixel(superficie, x, y, cor):
    superficie.set_at((int(x), int(y)), cor)

def draw_line(superficie, pontos, cor):
    for (x, y) in pontos:
        set_pixel(superficie, x, y, cor)

def draw_polygonon(superficie, vertices, color):
    n = len(vertices)
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i+1) % n]
        linha_bresenham(superficie, x0, y0, x1, y1, color)
  
def linha_bresenham(superficie, x0, y0, x1, y1, cor):
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
        set_pixel(superficie, x0, y0, cor)

def scanline_fill(superficie, pontos, cor_preenchimento):
    ys = [ p[1] for p in pontos] # Lista só de Y
    y_min = min(ys) 
    y_max = max(ys)

    n = len(pontos)

    for y in range(y_min, y_max): # do mínimo ao máximo de y, movimento vertical
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
                set_pixel(superficie, x, y, cor_preenchimento)