with open("code_advent_25\day1\input.txt", "r") as f:
    input = f.read().splitlines()
import numpy as np
c = 0
start_index = 0
current_index = start_index

instruction = "R110"

step_size = int(instruction[1:])

if instruction[0] == "L":
    step_size *= -1
n_loops = abs(step_size)//100
c += n_loops
real_step = abs(step_size)%100*np.sign(step_size)
print("reak", real_step)

if current_index + real_step >= 100 and current_index != 0:
    c += 1
    print("pos")
elif current_index + real_step <= 0 and current_index != 0:
    c += 1
    print("neg")


print(n_loops, step_size)
current_index = (current_index + step_size) % 100


print(c)
 