import json
from math3D import Vector3, vector_mul_scalar, vector_normalize
from objects import Sphere, Wall


def v3(a):
    return Vector3(float(a[0]), float(a[1]), float(a[2]))


def hex_to_v3(s):
    """'#rrggbb' -> Vector3(r,g,b) en 0..255"""
    s = s.strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s) != 6:
        raise ValueError(f"Couleur invalide: {s}")
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return Vector3(r, g, b)


def load_list_scene(path):
    """
    Retourne: objects(list), lights(list)
    lights = dicts simples:
      {"type":"ambient", "intensity":0.2}
      {"type":"point", "intensity":0.6, "position":Vector3(...)}
      {"type":"directional", "intensity":0.2, "direction":Vector3(...)}  (optionnel)
    """
    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)

    if not isinstance(items, list):
        raise ValueError("Le JSON doit être une liste [...]")

    objects = []
    lights = []

    for it in items:
        t = it.get("type", "").lower()

        if t == "sphere":
            center = v3(it["coords"])
            radius = float(it["radius"])
            color = hex_to_v3(it["color"])
            spec = int(it.get("specular", 0))
            refl = float(it.get("reflective", 0.0))
            objects.append(Sphere(center, radius, color, specular=spec, reflective=refl))

        elif t == "wall":
            n = vector_normalize(v3(it["normal"]))
            d = float(it.get("d", 0.0))
            # Plan: n·x + d = 0 -> on peut choisir un point du plan: P0 = -d * n
            point = vector_mul_scalar(n, -d)
            color = hex_to_v3(it["color"])
            spec = int(it.get("specular", 0))
            refl = float(it.get("reflective", 0.0))
            objects.append(Wall(point, n, color, specular=spec, reflective=refl))

        elif t == "light":
            kind = it.get("kind", "").lower()
            intensity = float(it["intensity"])

            if kind == "ambient":
                lights.append({"type": "ambient", "intensity": intensity})

            elif kind == "point":
                pos = v3(it["coords"])
                lights.append({"type": "point", "intensity": intensity, "position": pos})

            elif kind == "directional":
                direction = v3(it["direction"])
                lights.append({"type": "directional", "intensity": intensity, "direction": direction})

            else:
                raise ValueError(f"Kind de light inconnu: {kind}")

        else:
            raise ValueError(f"Type inconnu: {t}")

    return objects, lights
