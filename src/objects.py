import math
from math3D import (
    dot_product,
    vector_sub,
    vector_add,
    vector_mul_scalar,
    vector_length,
    vector_normalize
)


#Definition des objets de la scene

class Sphere:
    def __init__(self, center, radius, color, specular=0, reflective=0.0):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
        self.reflective = reflective

    def intersect(self, ray):
        """
        Calcule l'intersection rayon/sphere
        Retourne la distance t > 0 ou None
        """
        oc = vector_sub(ray.origin, self.center)

        a = dot_product(ray.direction, ray.direction)
        b = 2 * dot_product(oc, ray.direction)
        c = dot_product(oc, oc) - self.radius * self.radius

        delta = b * b - 4 * a * c
        if delta < 0:
            return None

        sqrt_delta = math.sqrt(delta)
        t1 = (-b - sqrt_delta) / (2 * a)
        t2 = (-b + sqrt_delta) / (2 * a)

        if t1 > 0:
            return t1
        if t2 > 0:
            return t2
        return None

    def normal_at(self, point):
        """ Retourne la normale au point d'intersection """
        return vector_normalize(vector_sub(point, self.center))


class Wall:
    def __init__(self, point, normal, color, specular=0, reflective=0.0):
        self.point = point
        self.normal = vector_normalize(normal)
        self.color = color
        self.specular = specular
        self.reflective = reflective

    def intersect(self, ray):
        """ Intersection rayon/plan """
        denom = dot_product(ray.direction, self.normal)

        if abs(denom) < 1e-6:
            return None

        t = dot_product(vector_sub(self.point, ray.origin), self.normal) / denom

        if t > 0:
            return t
        return None

    def normal_at(self, point):
        """ La normale est la meme partout sur un plan """
        return self.normal