import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)  # fallback to CPU if GPU not available
rng = np.random.default_rng()
RES = 500     # logical resolution (bigger pixels)
WINDOW_RES = 1012 # window size
BRUSH_RADIUS = 10
current_material = 1 # 0 air, 1 sand, 2 stone

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
            img[i, j] = ti.Vector([225/255, 193/255, 110/255])      # sand
        elif v == 2:
            img[i, j] = ti.Vector([0.5,0.5,0.5])      # stone
        elif v == 3:
            img[i, j] = ti.Vector([0.0, 0.0, 1.0])      # water
        elif v == 4:
            img[i, j] = ti.Vector([1.0, 1.0, 0.0])      # yellow
        elif v == 5:
            img[i, j] = ti.Vector([1.0, 0.0, 1.0])      # magenta


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
def stone():
    for i, j in canvas:
        if canvas[i,j] == 2:
            pass

@ti.kernel
def water():
    for i, j in canvas:
        if canvas[i,j] == 3:
            if canvas[i,j-1] == 0 and j != 0:
                canvas[i,j] = 0
                canvas[i,j-1] = 3
            elif canvas[i,j-1] == 3:
                if ti.random(float) > 0.5:
                    if canvas[i-1,j] == 0 and i-1 != 0:
                        canvas[i,j] = 0
                        canvas[i-1,j] = 3
                    elif canvas[i+1,j] == 0 and i+1 != RES:
                      canvas[i,j] = 0
                      canvas[i+1,j] = 3
                elif canvas[i+1,j] == 0 and i+1 != RES:
                    canvas[i,j] = 0
                    canvas[i+1,j] = 3
                elif canvas[i-1,j] == 0 and i-1 != 0:
                    canvas[i,j] = 0
                    canvas[i-1,j] = 3
                

@ti.kernel
def sand_fall():
    for i, j in canvas:
        if canvas[i,j] == 1:
            if j == 0:
                pass
            elif canvas[i,j-1] == 0:
                canvas[i,j] = 0
                canvas[i,j-1] = 1
            elif ti.random(float) > 0.5:
                if canvas[i-1,j-1] == 0 and i-1 != 0:
                    canvas[i,j] = 0
                    canvas[i-1,j-1] = 1
                elif canvas[i+1,j-1] == 0 and i+1 != RES:
                    canvas[i,j] = 0
                    canvas[i+1,j-1] = 1
            elif canvas[i-1,j-1] == 0 and i-1 != 0:
                    canvas[i,j] = 0
                    canvas[i-1,j-1] = 1
            elif canvas[i+1,j-1] == 0 and i+1 != RES:
                    canvas[i,j] = 0
                    canvas[i+1,j-1] = 1
clear()



while window.running:
    if window.is_pressed("w"):
        current_material = 2
    if window.is_pressed("q"):
        current_material = 1
    if window.is_pressed("e"):
        current_material = 3
    if window.is_pressed(ti.ui.LMB):
        mx, my = window.get_cursor_pos()
        x = int(mx * RES)
        y = int(my * RES)  # flip y-axis
        paint(x, y, current_material)
    if window.is_pressed('c'):
        clear()
    sand_fall()
    water()
    colorize()
    canvas_ui.set_image(img)
    window.show()

