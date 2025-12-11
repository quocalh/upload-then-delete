from OpenGL.GL import *

# IDK man XD, not WIP

def ASSERT(x):
    if not x:
        exit()

def GLClearError():
    while glGetError() != GL_NO_ERROR:
        pass

def Run(function, file, line):
    error = GLClearError()
    if error != GL_NO_ERROR:
        print(f"[OPENGL FUCKED UP]: {error} in line {line}, file {file}")
        return False
    return True