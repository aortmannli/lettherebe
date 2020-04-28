import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)

    ambient = calculate_ambient(ambient, areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)

    r = ambient[0] + diffuse[0] + specular[0]
    g = ambient[1] + diffuse[1] + specular[1]
    b = ambient[2] + diffuse[2] + specular[2]

    return limit_color([r,g,b])

def calculate_ambient(alight, areflect):
    return vector_mult(alight, areflect)

def calculate_diffuse(light, dreflect, normal):
    color = dot_product(normal, light[LOCATION])

    r = light[COLOR][0] * dreflect[0] * color
    g = light[COLOR][1] * dreflect[1] * color
    b = light[COLOR][2] * dreflect[2] * color

    return limit_color([r, g, b])

def calculate_specular(light, sreflect, view, normal):
    normalize(light[0])
    normalize(normal)
    t = scale(normal, 2 * dot_product(light[0], normal))
    s = dot_product(matrix_subtraction(t, light[0]), view)
    s = s ** 2
    out = scale(sreflect, s)
    return vector_mult(light[1], out)

def limit_color(color):
    if color > 255:
        return 255
    elif color < 0:
        return 0
    return color

def vector_mult(a, b):
    out = []
    i = 0
    while i < len(a):
        out.append(a[i] * b[i])
        i += 1
    return out
def matrix_addition(a, b):
    out = []
    i = 0
    while i < len(a):
        out.append(a[i] + b[i])
        i += 1
    return out

def matrix_subtraction(a, b):
    out = []
    i = 0
    while i < len(a):
        out.append(a[i] - b[i])
        i += 1
    return out
def scale(vector, scalar):
    out = []
    i = 0
    while i < len(vector):
        out.append(vector[i] * scalar)
        i += 1
    return out
#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
