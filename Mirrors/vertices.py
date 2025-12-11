import numpy as np
from Pipeline.VAO import * 
from Pipeline.VBO import * 

from numba.experimental import *
import numba as nb

from numba import jit, njit

# spec = [
#     ("Vertices", nb.float32[:]),
#     ("Indices", nb.uint[:]),
#     ("layout", nb.)
# ]
# @jitclass
class NetMesh:
    def __init__(self, Vertices, Indices, Layout: VBO_Layout):
        self.Vertices = Vertices
        self.Indices = Indices
        self.layout = Layout

@njit
def CreateIndicesJIT(V: int, U: int):
    Indices = []
    for z in range(V - 1):
        for x in range(U - 1):
            stage = z * U
            # First triangle
            Indices.extend([stage + x, 
                            stage + x + U,   
                            stage + x + U + 1])
            # Second triangle
            Indices.extend([stage + x, 
                            stage + x + U + 1, 
                            stage + x + 1])
    Indices = np.array(Indices, dtype=np.uint32)
    return Indices

@njit
def CreateVerticesJIT(V: int, U: int, Unit: float, v3Color: list[3] = (0.4, 0.6, 0.9)):
    Vertices = np.empty((V * U, 9), dtype=np.float32)
    for z in range(V):
        for x in range(U):
            index = z * U + x
            Vertices[index] = [x * Unit, 0, z * Unit, 0, 1, 0, v3Color[0], v3Color[1], v3Color[2]]
    return Vertices


def CreateVertices(U: int, V: int, Unit = 1, v3Color: list[3] = (0.4, 0.6, 0.9)):
    # Create Vertices
    Vertices = CreateVerticesJIT(V, U, Unit, v3Color)

    # Create IBO
    Indices = CreateIndicesJIT(V, U)

    # Create layout
    layout = VBO_Layout(); layout.AddLayout(3); layout.AddLayout(3); layout.AddLayout(3)
    
    return NetMesh(Vertices, Indices, layout)


