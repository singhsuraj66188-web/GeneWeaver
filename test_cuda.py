
import numpy as np
from numba import cuda

@cuda.jit
def add_one(values):
    i = cuda.grid(1)
    if i < values.size:
        values[i] += 1

data = np.arange(8, dtype=np.int32)

device_data = cuda.to_device(data)
add_one[1, 8](device_data)

result = device_data.copy_to_host()

print("Original array:", data)
print("GPU result:", result)
print("CUDA kernel executed successfully!")
