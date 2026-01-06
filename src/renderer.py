from math3D import (
    Vector3,
    vector_add, vector_sub, vector_mul_scalar,
    vector_length, vector_normalize, dot_product,
    reflect, distance
)
from ray import Ray

# -------------------------
# Camera + Image FIXES ici
# -------------------------
WIDTH = 400
HEIGHT = 300

CAMERA_POS = Vector3(0, 0, -3)

VIEWPORT_H = 1.0
VIEWPORT_W = WIDTH / HEIGHT
VIEWPORT_D = 1.0

BACKGROUND = Vector3(0, 0, 0)
MAX_DEPTH = 3

INF = 10**9
EPS = 1e-3


def clamp_color(c):
    return Vector3(
        max(0, min(255, c.x)),
        max(0, min(255, c.y)),
        max(0, min(255, c.z)),
    )


def canvas_to_viewport(cx, cy):
    # (cx * vw / w, cy * vh / h, d)
    return Vector3(
        cx * VIEWPORT_W / WIDTH,
        cy * VIEWPORT_H / HEIGHT,
        VIEWPORT_D
    )


def closest_intersection(ray, objects):
    closest_t = INF
    closest_obj = None
    for obj in objects:
        t = obj.intersect(ray)
        if t is not None and t > EPS and t < closest_t:
            closest_t = t
            closest_obj = obj
    return closest_obj, closest_t


def is_in_shadow(P, L, t_max, objects):
    shadow_ray = Ray(P, L)  # direction normalisée dans Ray
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
            L = vector_sub(light["position"], P)
            t_max = distance(P, light["position"])  # comme direction est normalisée -> t = distance
        else:  # directional
            L = light["direction"]
            t_max = INF

        # Ombre
        if is_in_shadow(P, L, t_max, objects):
            continue

        L_dir = vector_normalize(L)

        # Diffuse: max(0, N·L)
        n_dot_l = dot_product(N, L_dir)
        if n_dot_l > 0:
            intensity += light["intensity"] * n_dot_l

        # Spéculaire (optionnel)
        if specular and specular > 0:
            minus_L = vector_mul_scalar(L_dir, -1)         # direction "entrante"
            R = vector_normalize(reflect(minus_L, N))      # reflet
            r_dot_v = dot_product(R, V)
            if r_dot_v > 0:
                intensity += light["intensity"] * (r_dot_v ** specular)

    return intensity


def trace_ray(ray, depth, objects, lights):
    obj, t = closest_intersection(ray, objects)
    if obj is None:
        return BACKGROUND

    P = ray.point_at(t)
    N = obj.normal_at(P)
    V = vector_sub(CAMERA_POS, P)

    # Couleur locale
    light_i = compute_lighting(P, N, V, obj.specular, lights, objects)
    local_color = vector_mul_scalar(obj.color, light_i)

    # Réflexion
    r = obj.reflective
    if depth <= 0 or r <= 0.0:
        return clamp_color(local_color)

    R_dir = reflect(ray.direction, vector_normalize(N))
    new_origin = vector_add(P, vector_mul_scalar(vector_normalize(N), EPS))

    reflected = trace_ray(Ray(new_origin, R_dir), depth - 1, objects, lights)

    c1 = vector_mul_scalar(local_color, (1.0 - r))
    c2 = vector_mul_scalar(reflected, r)
    return clamp_color(vector_add(c1, c2))


def save_ppm(filename, pixels):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("P3\n")
        f.write(f"{WIDTH} {HEIGHT}\n")
        f.write("255\n")
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                c = clamp_color(pixels[y][x])
                row.append(f"{int(c.x)} {int(c.y)} {int(c.z)}")
            f.write(" ".join(row) + "\n")


def render(objects, lights, output="output.ppm"):
    pixels = [[BACKGROUND for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for y in range(HEIGHT):
        for x in range(WIDTH):
            cx = x - WIDTH / 2
            cy = HEIGHT / 2 - y

            direction = canvas_to_viewport(cx, cy)
            ray = Ray(CAMERA_POS, direction)

            pixels[y][x] = trace_ray(ray, MAX_DEPTH, objects, lights)

    save_ppm(output, pixels)
