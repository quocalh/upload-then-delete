import numpy as np

MirrorVertices = np.array(dtype=np.float32, object=[
    -1.0,  1.0, 0.0,   0.0, 0.0, 1.0, # Top-left
     1.0,  1.0, 0.0,   0.0, 0.0, 1.0, # Top-right
    -1.0, -1.0, 0.0,   0.0, 0.0, 1.0, # Bottom-left
     1.0, -1.0, 0.0,   0.0, 0.0, 1.0  # Bottom-right
])  # QUAD

MirrorIndices = np.array(dtype=np.int32, object=[
    0, 1, 2,  # First triangle
    2, 1, 3   # Second triangle
])
