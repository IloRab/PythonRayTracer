import sys
from scene_loader import load_list_scene
from renderer import render


def main():
    if len(sys.argv) < 2:
        print("Erreur : il manque le fichier de la scene")
        return

    filepath = sys.argv[1]
    objects, lights = load_list_scene(filepath)
    render(objects, lights, output="output.ppm")

    print("Rendu termine !")


if __name__ == "__main__":
    main()