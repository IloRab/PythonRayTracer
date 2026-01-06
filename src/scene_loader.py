from math3D import Vector3
from objects import Sphere, Wall


def load_list_scene(path):
    """
    Lit le fichier texte et creer les objets de la scene
    """
    objects = []
    lights = []

    print(f"Chargement de : {path}")

    try:
        with open(path, "r") as f:
            for line in f:
                #On ignore les commentaires et les lignes vides
                line = line.split('#')[0].strip()
                if not line:
                    continue

                parts = line.split()
                obj_type = parts[0].upper()

                if obj_type == "SPHERE":
                    center = Vector3(float(parts[1]), float(parts[2]), float(parts[3]))
                    radius = float(parts[4])
                    color = Vector3(float(parts[5]), float(parts[6]), float(parts[7]))

                    spec = int(parts[8]) if len(parts) > 8 else 0
                    refl = float(parts[9]) if len(parts) > 9 else 0.0

                    objects.append(Sphere(center, radius, color, spec, refl))

                elif obj_type == "WALL":
                    point = Vector3(float(parts[1]), float(parts[2]), float(parts[3]))
                    normal = Vector3(float(parts[4]), float(parts[5]), float(parts[6]))
                    color = Vector3(float(parts[7]), float(parts[8]), float(parts[9]))

                    spec = int(parts[10]) if len(parts) > 10 else 0
                    refl = float(parts[11]) if len(parts) > 11 else 0.0

                    objects.append(Wall(point, normal, color, spec, refl))

                elif obj_type == "LIGHT":
                    l_type = parts[1].lower()
                    intensity = float(parts[2])

                    if l_type == "ambient":
                        lights.append({"type": "ambient", "intensity": intensity})

                    elif l_type == "point":
                        pos = Vector3(float(parts[3]), float(parts[4]), float(parts[5]))
                        lights.append({"type": "point", "intensity": intensity, "position": pos})

                    elif l_type == "directional":
                        d = Vector3(float(parts[3]), float(parts[4]), float(parts[5]))
                        lights.append({"type": "directional", "intensity": intensity, "direction": d})

    except FileNotFoundError:
        print(f"Erreur : Impossible de trouver le fichier {path}")
        return [], []

    return objects, lights