import taichi as ti
import numpy as np

ti.init(arch=ti.cpu)  # fallback to CPU if GPU not available
rng = np.random.default_rng()
RES = 1000    # logical resolution (bigger pixels)
WINDOW_RES = 1000 # window size
BRUSH_RADIUS = 20
current_material = 1 # 0 air, 1 sand, 2 stone
offset = 0
canvas = ti.field(dtype=ti.f32, shape=(RES, RES))
write_canvas = ti.field(dtype=ti.f32, shape=(RES, RES)) #double buffer


window = ti.ui.Window("Taichi Paint Field", (WINDOW_RES, WINDOW_RES))
img = ti.Vector.field(3, dtype=ti.f32, shape=(RES, RES))

canvas_ui = window.get_canvas()

@ti.kernel
def colorize():
    for i, j in canvas:
        v = ti.cast(canvas[i, j], ti.i32)
        if v == 0:
            img[i, j] = ti.Vector([0.0, 0.0, 0.0])      # black
        
        elif v == 1:
            if ti.random(float) > 0.5:
                img[i, j] = ti.Vector([225/255, 193/255, 110/255])# sand
            else:
                img[i, j] = ti.Vector([200/255, 180/255, 130/255])
          #  img[i, j] = ti.Vector([ti.random(float),ti.random(float),ti.random(float)])      # sand




@ti.kernel
def paint(x: ti.i32, y: ti.i32, current_material: ti.i32):
    for i, j in canvas:
        if (i - x) ** 2 + (j - y) ** 2 <= BRUSH_RADIUS ** 2:
            canvas[i, j] = current_material  # white

@ti.kernel
def clear():
    for i, j in canvas:
        write_canvas[i, j] = 0.0  # black

@ti.kernel
def sand_fall(offset: ti.i32):
    for bi, bj in ti.ndrange(RES // 2, RES // 2):
        i = 2 * bi + offset
        j = 2 * bj + offset
    
        a1 = a0 = ti.i32(canvas[i,j])
        b1 = b0 = ti.i32(canvas[i+1,j])
        c1 = c0= ti.i32(canvas[i,j+1])
        d1 = d0 = ti.i32(canvas[i+1,j+1])

        if a0 == 0 and c0 == 1 and j != 0:
            a1 = 1
            c1 = 0
        elif c0 == 1 and a0 == 1 and b0 == 0 and d0 == 0 and i+1 != RES:
            c1 = 0
            b1 = 1

        if d0 == 1 and b0 == 0 and j != 0:
            d1 = 0
            b1 = 1
        elif d0 == 1 and b0 == 1 and a0 == 0 and c0 == 0 and i != 0:
            d1 = 0
            a1 = 1

        canvas[i,j] = a1
        canvas[i+1,j] = b1
        canvas[i,j+1] = c1
        canvas[i+1,j+1] = d1



clear()



while window.running:
    for _ in range(5):
        sand_fall(offset)
        offset ^= 1
    if window.is_pressed(ti.ui.LMB):
        mx, my = window.get_cursor_pos()
        x = int(mx * RES)
        y = int(my * RES)  # flip y-axis
        paint(x, y, current_material)
    if window.is_pressed('c'):
        clear()
    colorize()
    canvas_ui.set_image(img)
    window.show()