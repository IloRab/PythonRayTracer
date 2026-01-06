import math
from dataclasses import dataclass

@dataclass
class Vector3:
    x: float
    y: float
    z: float


def vector_neg(A):
    """Inverse de vecteur"""
    return Vector3(-A.x,-A.y,A.z)

def vector_add(A, B):
    """Addition de deux vecteurs"""
    return Vector3(A.x + B.x, A.y + B.y, A.z + B.z)

def distance(A, B):
    """Distance entre deux points"""
    return vector_length(vector_sub(A,B))

def vector_sub(A, B):
    """Soustraction de deux vecteurs"""
    return Vector3(A.x - B.x, A.y - B.y, A.z - B.z)

def vector_mul_scalar(A,s):
    """Multiplication par scalaire"""
    return Vector3(A.x*s,A.y*s,A.z*s)

def dot_product(A, B):
    """Calcule le produit scalaire entre deux vecteurs A et B."""
    return A.x * B.x + A.y * B.y + A.z * B.z

def vector_length(vector):
    """Calcule la longueur d'un vecteur."""
    return math.sqrt(dot_product(vector, vector))

def vector_normalize(vector):
    """Normalise un vecteur pour obtenir un vecteur de longueur 1."""
    length = vector_length(vector)
    if length != 0:
        normalized_vector = Vector3(vector.x / length, vector.y / length, vector.z / length)
    else:
        normalized_vector = Vector3(0, 0, 0)
    return normalized_vector

def cross_product(A, B):
    """Calcule le produit vectoriel A x B."""
    return Vector3(
        A.y * B.z - A.z * B.y,
        A.z * B.x - A.x * B.z,
        A.x * B.y - A.y * B.x
)
def reflect(V, N):
    """Reflection avec V le rayon et N la normale de destination Formule : R = V-2(V.N)N"""
    return vector_sub(V, vector_mul_scalar(N,2*dot_product(V,N)))
