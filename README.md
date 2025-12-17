# PythonRayTracer

RABIARIVELO Ilo Andrianaly 3FI-3I | RAMAKICHENIN Jeevan 3FI-3I

Projet RayTracer Outils Mathématiques 3D

Les imports :

pyray
math

Plan pour le code :

1. Base math : vecteur 3D (math3D.py OK)
2. Représenter un rayon (ray.py OK)
3. Object et intersections : (objects.py OK)

   - Sphere (OK)
   - Wall (OK)

4. Caméra et generation des rayons (renderer.py)
   Paramètres caméra : position, viewport, projection (orthographique/perspective)
   Fonction compute_ray(x, y) (pixel → rayon)

5. L'object lumière (light.py)
   Classes :
   AmbientLight(intensity)
   PointLight(position, intensity)
   (optionnel) DirectionalLight(direction, intensity)

6. Création du rendu (boucle pixels) (renderer.py)
   render(scene, camera, width, height) :
   boucle sur pixels
   génère un rayon
   calcule la couleur via shading + ombres + réflexions
   écrit dans l’image

7. Shading (calcule la couleur d’un point)(renderer.py (ou petit shading.py si tu veux séparer))
   shade(hit, scene, ray, depth) :
   lumière ambiante + diffuse + spéculaire
   clamp couleur [0..255] ou [0..1]
   Utilise reflect() du math3D.py

8. Ombres (renderer.py)
   is_in_shadow(point, light) :
   crée un “shadow ray” vers la lumière
   si intersection avant la lumière → ombre

9. Réflexions sur les sphères (renderer.py)
   récursion : trace_ray(ray, depth)
   si matériau reflective > 0 :
   rayon réfléchi
   mélange couleur locale et couleur réfléch

10. Chargement de la scène avec l'entrée JSON (scene_loader.py)
    lit le json (liste d’objets)
    instancie Sphere/Wall + lumières
    renvoie un Scene (ou juste objects, lights, camera)
    Exemple d'entrée JSON dans input/in_exemple.json

11. Export de l'image en PPM (image.py)
    structure Image(width,height)
    set_pixel(x,y,color)
    save_ppm(path) (ou PNG si vous avez une lib)

12. Main
    main.py
    charge json via scene_loader
    appelle renderer.render(...)
    sauvegarde via image.save_ppm(...)
