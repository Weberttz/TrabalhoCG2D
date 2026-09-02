def set_pixel(superficie, x, y, cor):
    superficie.set_at((int(x), int(y)), cor)
  
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