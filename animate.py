import os
import math
import time

# Config
FRAMES = 48
FOLDER = "frames"
CMD = "python3"  #juste python si on est sur windows


def rotate(x, z, angle):
    #centre de la pyramide environ à Z=4.8
    cx, cz = 0, 4.8

    # Formule de rotation 2D autour d'un point
    dx = x - cx
    dz = z - cz

    nx = dx * math.cos(angle) - dz * math.sin(angle)
    nz = dx * math.sin(angle) + dz * math.cos(angle)

    return nx + cx, nz + cz

def main():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    # Position de depart des 4 spheres
    spheres = [
        (0, 2.0, 5.0, "230 230 230"), #haut mirroir
        (0, 0.2, 3.5, "200 25 25"), #cnetre rouge
        (-1.3, 0.2, 5.8, "200 180 25"), #gauche jaune
        (1.3, 0.2, 5.8, "25 50 230") #droite bleu
    ]

    print(f"Generation de {FRAMES} frames en cours...")
    start_time = time.time()

    for i in range(FRAMES):
        #angle actuel
        angle = (2 * math.pi * i) / FRAMES

        #on ecrit d'abord tout ce qui est statique (Lumieres + Murs)
        content = """
# Frame generate
LIGHT ambient 0.2
LIGHT point 0.6 -5 8 0
LIGHT point 0.4 5 5 -2
LIGHT point 0.3 0 5 8

WALL 0 -1 0 0 1 0 50 50 50 50 0.4
WALL 0 10 0 0 -1 0 0 0 0 0 0
WALL 0 0 12 0 0 -1 25 25 25 0 0
WALL -6 0 0 1 0 0 200 100 25 0 0
WALL 6 0 0 -1 0 0 25 100 200 0 0
"""
        #on ajoute les spheres dynamiquement
        content += "\n# Spheres (Rotated)\n"
        for sx, sy, sz, color in spheres:
            rx, rz = rotate(sx, sz, angle)
            #on formatte la ligne SPHERE directement ici
            content += f"SPHERE {rx:.2f} {sy:.2f} {rz:.2f} 1.2 {color} 50 0.5\n"

        #Ecriture du fichier temporaire
        with open("scene_tmp.txt", "w") as f:
            f.write(content)

        #lancement du rendu
        print(f"[{i + 1}/{FRAMES}] Rendu en cours...")
        os.system(f"{CMD} src/main.py scene_tmp.txt > log_rendu.txt")

        #gestion de l'image de sortie
        target = f"{FOLDER}/frame_{i:02d}.ppm"
        if os.path.exists("output.ppm"):
            if os.path.exists(target):
                os.remove(target)
            os.rename("output.ppm", target)
        else:
            print("Erreur: Pas d'image output.ppm générée !")
            break

    #Nettoyage
    if os.path.exists("scene_tmp.txt"): os.remove("scene_tmp.txt")
    if os.path.exists("log_rendu.txt"): os.remove("log_rendu.txt")

    print(f"Terminé en {time.time() - start_time:.1f} secondes.")


if __name__ == "__main__":
    main()