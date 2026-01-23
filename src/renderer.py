from math3D import (
    Vector3,
    vector_add, vector_sub, vector_mul_scalar,
    vector_normalize, reflect
)
from ray import Ray
from image import save_ppm
from lighting import compute_lighting

WIDTH = 800
HEIGHT = 600

CAMERA_POS = Vector3(0, 0, -3)

VIEWPORT_H = 1.0
VIEWPORT_W = WIDTH / HEIGHT
VIEWPORT_D = 1.0

BACKGROUND = Vector3(0, 0, 0)
MAX_DEPTH = 3
INF = 10 ** 9
EPS = 1e-3

def clamp_color(c):
    """ Force les couleurs entre 0 et 255 """
    return Vector3(
        max(0, min(255, c.x)),
        max(0, min(255, c.y)),
        max(0, min(255, c.z)),
    )

def canvas_to_viewport(cx, cy):
    return Vector3(
        cx * VIEWPORT_W / WIDTH,
        cy * VIEWPORT_H / HEIGHT,
        VIEWPORT_D
    )

def closest_intersection(ray, objects):
    """ Trouve l'objet le plus proche touche par le rayon """
    closest_t = INF
    closest_obj = None
    for obj in objects:
        t = obj.intersect(ray)
        if t is not None and t > EPS and t < closest_t:
            closest_t = t
            closest_obj = obj
    return closest_obj, closest_t

def trace_ray(ray, depth, objects, lights):
    obj, t = closest_intersection(ray, objects)

    if obj is None:
        return BACKGROUND

    P = ray.point_at(t)
    N = obj.normal_at(P)
    V = vector_sub(CAMERA_POS, P)

    light_i = compute_lighting(P, N, V, obj.specular, lights, objects)
    local_color = vector_mul_scalar(obj.color, light_i)

    r = obj.reflective
    if depth <= 0 or r <= 0.0:
        return clamp_color(local_color)

    R_dir = reflect(ray.direction, vector_normalize(N))
    new_origin = vector_add(P, vector_mul_scalar(vector_normalize(N), EPS))

    reflected_color = trace_ray(Ray(new_origin, R_dir), depth - 1, objects, lights)

    c1 = vector_mul_scalar(local_color, (1.0 - r))
    c2 = vector_mul_scalar(reflected_color, r)
    return clamp_color(vector_add(c1, c2))


def render(objects, lights, output="output.ppm"):
    print(f"Calcul de l'image {WIDTH}x{HEIGHT}...")
    pixels = [[BACKGROUND for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for y in range(HEIGHT):
        for x in range(WIDTH):
            cx = x - WIDTH / 2
            cy = HEIGHT / 2 - y

            direction = canvas_to_viewport(cx, cy)
            ray = Ray(CAMERA_POS, direction)

            pixels[y][x] = trace_ray(ray, MAX_DEPTH, objects, lights)

    save_ppm(output, pixels, WIDTH, HEIGHT)