from math3D import (
    vector_sub, vector_normalize, dot_product,
    vector_mul_scalar, reflect, distance
)
from ray import Ray

#Constantes pour les calculs de lumiere
INF = 10 ** 9
EPS = 1e-3


def is_in_shadow(P, L, t_max, objects):
    """Renvoie True si un objet bloque la lumiere"""
    shadow_ray = Ray(P, L)
    for obj in objects:
        t = obj.intersect(shadow_ray)
        #On verifie si l'intersection est valide et avant la lumiere
        if t is not None and t > EPS and t < t_max:
            return True
    return False


def compute_lighting(P, N, V, specular, lights, objects):
    """
    Calcule l'intensite lumineuse reçue au point P
    Somme de l'ambiance + diffuse + speculaire
    """
    intensity = 0.0
    N = vector_normalize(N)
    V = vector_normalize(V)

    for light in lights:
        if light["type"] == "ambient":
            intensity += light["intensity"]
            continue

        #Definition du vecteur Lumiere (L) et distance max
        if light["type"] == "point":
            L = vector_sub(light["position"], P)
            t_max = distance(P, light["position"])
        elif light["type"] == "directional":
            L = light["direction"]
            t_max = INF
        else:
            continue

        #Test d'ombre
        if is_in_shadow(P, L, t_max, objects):
            continue

        L_dir = vector_normalize(L)

        #Intensite selon l'angle entre la normale et la lumiere
        n_dot_l = dot_product(N, L_dir)
        if n_dot_l > 0:
            intensity += light["intensity"] * n_dot_l

        #Calcul Speculaire (Reflet brillant)
        if specular > 0:
            # On cherche le vecteur reflechi de la lumiere par rapport a la normale
            minus_L = vector_mul_scalar(L_dir, -1)
            R = vector_normalize(reflect(minus_L, N))

            #Plus R est aligne avec la vue (V), plus ça brille
            r_dot_v = dot_product(R, V)
            if r_dot_v > 0:
                intensity += light["intensity"] * (r_dot_v ** specular)

    return intensity