
#Charge la scène (JSON)
#Crée la caméra 
#appelle le renderer
#sauvegarde l'image

import sys
from scene_loader import load_list_scene
from renderer import render
from math3D import Vector3


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py input/scene.json")
        return

    objects, lights = load_list_scene(sys.argv[1])
    render(objects, lights, output="output.ppm")
    print("OK -> output.ppm")


if __name__ == "__main__":
    main()
