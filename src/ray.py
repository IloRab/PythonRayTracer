#Definition d'un rayon :
#représenter un rayon
#donner un point sur le rayon

from math3D import vector_add, vector_mul_scalar, vector_normalize

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = vector_normalize(direction)

    def point_at(self, t):
        """Retourne le point O + tD"""
        return vector_add(self.origin, vector_mul_scalar(self.direction, t))
