import taichi as ti
import time
import numpy as np

# Test parameters
RES = 1000
ITERATIONS = 100

def benchmark_cpu():
    ti.init(arch=ti.cpu)
    canvas = ti.field(dtype=ti.f32, shape=(RES, RES))

    @ti.kernel
    def sand_fall_cpu(offset: ti.i32):
        for bi, bj in ti.ndrange(RES // 2, RES // 2):
            i = 2 * (RES//2 - 1 - bi) + offset
            j = 2 * bj + offset

            a0 = ti.i32(canvas[i,j])
            b0 = ti.i32(canvas[i+1,j])
            c0 = ti.i32(canvas[i,j+1])
            d0 = ti.i32(canvas[i+1,j+1])

            a1, b1, c1, d1 = a0, b0, c0, d0

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

    # Initialize with some sand
    canvas.fill(0.0)
    for i in range(100, 200):
        for j in range(100, 200):
            canvas[i, j] = 1.0

    start_time = time.time()
    offset = 0
    for _ in range(ITERATIONS):
        sand_fall_cpu(offset)
        offset ^= 1
    cpu_time = time.time() - start_time

    return cpu_time

def benchmark_gpu():
    ti.init(arch=ti.gpu)
    canvas = ti.field(dtype=ti.f32, shape=(RES, RES))

    @ti.kernel
    def sand_fall_gpu(offset: ti.i32):
        for bi, bj in ti.ndrange(RES // 2, RES // 2):
            i = 2 * (RES//2 - 1 - bi) + offset
            j = 2 * bj + offset

            a0 = ti.i32(canvas[i,j])
            b0 = ti.i32(canvas[i+1,j])
            c0 = ti.i32(canvas[i,j+1])
            d0 = ti.i32(canvas[i+1,j+1])

            a1, b1, c1, d1 = a0, b0, c0, d0

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

    # Initialize with some sand
    canvas.fill(0.0)
    for i in range(100, 200):
        for j in range(100, 200):
            canvas[i, j] = 1.0

    start_time = time.time()
    offset = 0
    for _ in range(ITERATIONS):
        sand_fall_gpu(offset)
        offset ^= 1
    gpu_time = time.time() - start_time

    return gpu_time

if __name__ == "__main__":
    print("Benchmarking CPU performance...")
    cpu_time = benchmark_cpu()
    print(".3f")

    print("Benchmarking GPU performance...")
    gpu_time = benchmark_gpu()
    print(".3f")

    speedup = cpu_time / gpu_time
    print(".2f")