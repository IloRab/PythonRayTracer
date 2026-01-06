def save_ppm(filename, pixels, width, height):
    print(f"Sauvegarde de l'image : {filename}")

    #On ouvre le fichier en mode écriture
    with open(filename, "w") as f:
        #Header du PPM (P3, dimensions, max value)
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")

        for y in range(height):
            row = []
            for x in range(width):
                c = pixels[y][x]

                #Conversion en entiers et limitation entre 0 et 255
                r = max(0, min(255, int(c.x)))
                g = max(0, min(255, int(c.y)))
                b = max(0, min(255, int(c.z)))

                row.append(f"{r} {g} {b}")

            # Ecriture de la ligne dans le fichier
            f.write(" ".join(row) + "\n")

    print("Image sauvegardée !")