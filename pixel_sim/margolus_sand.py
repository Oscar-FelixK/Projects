import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)  # fallback to CPU if GPU not available
rng = np.random.default_rng()
RES = 500  # logical resolution (bigger pixels)
WINDOW_RES = 500 # window size
BRUSH_RADIUS = 5
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
          #  if ti.random(float) > 0.5:
                img[i, j] = ti.Vector([225/255, 193/255, 110/255])# sand
        elif v == 2:
            img[i, j] = ti.Vector([0.5,0.5,0.5])# stone

      #      else:
             #   img[i, j] = ti.Vector([200/255, 180/255, 130/255])
          #  img[i, j] = ti.Vector([ti.random(float),ti.random(float),ti.random(float)])      # sand




@ti.kernel
def paint(x: ti.i32, y: ti.i32, current_material: ti.i32):
    for i, j in canvas:
        if (i - x) ** 2 + (j - y) ** 2 <= (BRUSH_RADIUS+ti.cast(ti.random() * 2, ti.i32)) ** 2:
            canvas[i, j] = current_material  # white

@ti.kernel
def clear():
    for i, j in canvas:
        write_canvas[i, j] = 0.0  # black

@ti.kernel
def sand_fall(i_offset: ti.i32, j_offset: ti.i32):
    for i, j in canvas:
        if (i + i_offset) % 2 == 0 and (j + j_offset) % 2 == 0:
    
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

@ti.kernel
def count_particles() -> ti.i32:
    sand_count = 0
    stone_count = 0
    for i, j in canvas:
        if canvas[i,j] == 1:
            sand_count += 1
        elif canvas[i,j] == 2:
            stone_count
    return sand_count 



#main loop:
offset_cycle = [[0,0],[1,1],[1,0],[0,1]]
cycle_index = 0
physics_running = False
pause_button_pressed_prev = False
pause_button_pressed = False
Frame = 0
n_ticks_per_frame = 2
while window.running:
    if physics_running:
        for _ in range(n_ticks_per_frame):
            i_offset = np.random.randint(0, 2)
            j_offset = np.random.randint(0, 2)
            sand_fall(i_offset, j_offset)
            cycle_index += 1
            if cycle_index >= 4:
                cycle_index = 0

    if window.is_pressed(ti.ui.SPACE):
        pause_button_pressed = True
        if pause_button_pressed_prev == False:
            physics_running = not physics_running
            pause_button_pressed_prev = True
    else:
        pause_button_pressed_prev = False
    if window.is_pressed(ti.ui.LMB):
        mx, my = window.get_cursor_pos()
        x = int(mx * RES)
        y = int(my * RES)  # flip y-axis
        paint(x, y, current_material)
    if window.is_pressed('q'):
        current_material = 1
    if window.is_pressed('w'):
        current_material = 2
    if window.is_pressed('e'):
        current_material = 0
    colorize()
    canvas_ui.set_image(img)
    window.show()
    sand_count = count_particles()
    Frame += 1
    print(f"\rNumber of Sand Particles: {sand_count:.2f}, Frame: {sand_count:.2f}", end="", flush=True)

