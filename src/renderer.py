from math3D import (
    Vector3,
    vector_add, vector_sub, vector_mul_scalar,
    vector_length, vector_normalize, dot_product,
    reflect, distance
)
from ray import Ray
from image import save_ppm

#---Parametres de la Camera et de l'Ecran---
WIDTH = 800
HEIGHT = 600

#On recule ça pos
CAMERA_POS = Vector3(0, 0, -3)

#Taille de la "fenetre" virtuelle devant la camera
VIEWPORT_H = 1.0
VIEWPORT_W = WIDTH / HEIGHT
VIEWPORT_D = 1.0

BACKGROUND = Vector3(0, 0, 0)  # Fond noir
MAX_DEPTH = 3

INF = 10 ** 9
EPS = 1e-3


def clamp_color(c):
    """ Force les couleurs entre 0 et 255 pour les calculs intermediaires """
    return Vector3(
        max(0, min(255, c.x)),
        max(0, min(255, c.y)),
        max(0, min(255, c.z)),
    )


def canvas_to_viewport(cx, cy):
    # Conversion coordonnées pixel (2D) -> Coordonnées espace (3D)
    return Vector3(
        cx * VIEWPORT_W / WIDTH,
        cy * VIEWPORT_H / HEIGHT,
        VIEWPORT_D
    )


def closest_intersection(ray, objects):
    """Trouve l'objet le plus proche touche par le rayon """
    closest_t = INF
    closest_obj = None
    for obj in objects:
        t = obj.intersect(ray)
        # On verifie t > EPS pour eviter le "noise"
        if t is not None and t > EPS and t < closest_t:
            closest_t = t
            closest_obj = obj
    return closest_obj, closest_t


def is_in_shadow(P, L, t_max, objects):
    """Lance un rayon vers la lumiere pour voir si on est cache """
    shadow_ray = Ray(P, L)
    for obj in objects:
        t = obj.intersect(shadow_ray)
        if t is not None and t > EPS and t < t_max:
            return True
    return False


def compute_lighting(P, N, V, specular, lights, objects):
    intensity = 0.0
    N = vector_normalize(N)
    V = vector_normalize(V)

    for light in lights:
        if light["type"] == "ambient":
            intensity += light["intensity"]
            continue

        if light["type"] == "point":
            # Vecteur vers la lumiere ponctuelle
            L = vector_sub(light["position"], P)
            t_max = distance(P, light["position"])
        else:
            #Lumiere directionnelle (soleil)
            L = light["direction"]
            t_max = INF

        #Gestion des Ombres
        if is_in_shadow(P, L, t_max, objects):
            continue

        L_dir = vector_normalize(L)

        n_dot_l = dot_product(N, L_dir)
        if n_dot_l > 0:
            intensity += light["intensity"] * n_dot_l

        #Speculaire (Blinn-Phong) : Reflet brillant
        if specular and specular > 0:
            minus_L = vector_mul_scalar(L_dir, -1)
            R = vector_normalize(reflect(minus_L, N))
            r_dot_v = dot_product(R, V)
            if r_dot_v > 0:
                intensity += light["intensity"] * (r_dot_v ** specular)

    return intensity


def trace_ray(ray, depth, objects, lights):
    obj, t = closest_intersection(ray, objects)

    #Si on ne touche rien, on renvoie la couleur du fond
    if obj is None:
        return BACKGROUND

    #Point d'intersection P et Normale N
    P = ray.point_at(t)
    N = obj.normal_at(P)
    V = vector_sub(CAMERA_POS, P)  # Vecteur vue

    #Calcul de la couleur locale
    light_i = compute_lighting(P, N, V, obj.specular, lights, objects)
    local_color = vector_mul_scalar(obj.color, light_i)

    #Gestion de la Reflexion
    r = obj.reflective
    if depth <= 0 or r <= 0.0:
        return clamp_color(local_color)

    # Calcul du rayon reflechi
    R_dir = reflect(ray.direction, vector_normalize(N))
    # Petite astuce (+EPS) pour ne pas se re-intersecter soi-meme
    new_origin = vector_add(P, vector_mul_scalar(vector_normalize(N), EPS))

    reflected_color = trace_ray(Ray(new_origin, R_dir), depth - 1, objects, lights)

    #Melange couleur locale et reflet
    c1 = vector_mul_scalar(local_color, (1.0 - r))
    c2 = vector_mul_scalar(reflected_color, r)
    return clamp_color(vector_add(c1, c2))


def render(objects, lights, output="output.ppm"):
    print(f"Calcul de l'image {WIDTH}x{HEIGHT}...")
    pixels = [[BACKGROUND for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for y in range(HEIGHT):
        for x in range(WIDTH):
            #On centre les coordonnees (0,0 au milieu de l'image)
            cx = x - WIDTH / 2
            cy = HEIGHT / 2 - y

            #On creer le rayon depuis la camera
            direction = canvas_to_viewport(cx, cy)
            ray = Ray(CAMERA_POS, direction)

            #Lancer du rayon
            pixels[y][x] = trace_ray(ray, MAX_DEPTH, objects, lights)

    # Sauvegarde avec le module separe (image.py)
    save_ppm(output, pixels, WIDTH, HEIGHT)