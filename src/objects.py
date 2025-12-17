#Definition des classes Sphere et Wall 
#Pour chaque objet ce sera : Parametre geometriques, materiau (couleur, specular (petite lumiere) et si reflectif (effet mirroir)) 

from math3D import (
    dot_product,
    vector_sub,
    vector_add,
    vector_mul_scalar,
    vector_length,
    vector_normalize
)
import math


class Sphere:
    def __init__(self, center, radius, color, specular=0, reflective=0.0):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
        self.reflective = reflective

    def intersect(self, ray):
        """
        Est ce qu'un rayon touche l'objet et si oui à quelle distance ?
        Retourne la distance t la plus proche (>0) ou None
        """
        oc = vector_sub(ray.origin, self.center)

        a = dot_product(ray.direction, ray.direction)
        b = 2 * dot_product(oc, ray.direction)
        c = dot_product(oc, oc) - self.radius * self.radius

        delta = b*b - 4*a*c
        if delta < 0:
            return None

        sqrt_delta = math.sqrt(delta)
        t1 = (-b - sqrt_delta) / (2*a)
        t2 = (-b + sqrt_delta) / (2*a)

        if t1 > 0:
            return t1
        if t2 > 0:
            return t2
        return None

    def normal_at(self, point):
        """
        Dans quelle direction “regarde” la surface à cet endroit précis ?
        Normale à la surface de la sphère
        """
        return vector_normalize(vector_sub(point, self.center))


class Wall:
    def __init__(self, point, normal, color, specular=0, reflective=0.0):
        self.point = point          # un point du plan
        self.normal = vector_normalize(normal)
        self.color = color
        self.specular = specular
        self.reflective = reflective

    def intersect(self, ray):
        """
        Est ce qu'un rayon touche l'objet et si oui à quelle distance ?
        Intersection rayon / plan
        """
        denom = dot_product(ray.direction, self.normal)
        if abs(denom) < 1e-6:
            return None  # rayon parallèle au plan

        t = dot_product(vector_sub(self.point, ray.origin), self.normal) / denom
        if t > 0:
            return t
        return None

    def normal_at(self, point):
        """
        Dans quelle direction “regarde” la surface à cet endroit précis ?
        Normale constante sur un plan
        """
        return self.normal
