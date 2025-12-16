# PythonRayTracer

RABIARIVELO Ilo Andrianaly 3FI-3I
RAMAKICHENIN Jeevan 3FI-3I

Projet RayTracer Outils Mathématiques 3D

Les imports :

Plan pour le code :

1. Base math : vecteur 3D (Normalement OK)
2. Représenter un rayon
3. Object et intersections :
   - Sphere
   - Wall
4. Caméra et generation des rayons
5. L'object lumière
6. Création du rendu (boucle pixels)
7. Shading (calcule la couleur d’un point)
8. Ombres
9. Réflexions sur les sphères(bonus)
10. Chargement de la scène avec l'entrée JSON
    Exemple d'entrée JSON

[
{"type":"sphere", "coords":[0,0,3], "radius":1, "color":"#ff0000"},
{"type":"sphere", "coords":[-2,0,4], "radius":1, "color":"#00ff00"},
{"type":"sphere", "coords":[2,0,4], "radius":1, "color":"#0000ff"},
{"type":"wall", "normal":[0,1,0], "d":1, "color":"#808080"},
{"type":"light", "kind":"ambient", "intensity":0.2},
{"type":"light", "kind":"point", "coords":[2,5,-2], "intensity":0.6}
]

11. Export de l'image en PPM
