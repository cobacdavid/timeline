__author__ = "david cobac"
__date__ = 20201019

from PIL import Image


def permute_tout(mon_image, j=0):
    dim_sous_image = mon_image.width - 2 * j
    indice_debut  = j
    indice_fin = indice_debut + dim_sous_image - 1
    #
    if dim_sous_image <= 1: return
    #
    for i in range(indice_fin - indice_debut):
        H = (indice_debut + i, j)
        D = (indice_fin, indice_debut + i)
        B = (indice_fin - i, indice_fin)
        G = (indice_debut, indice_fin - i)
        #
        h = mon_image.getpixel(H)
        d = mon_image.getpixel(D)
        b = mon_image.getpixel(B)
        g = mon_image.getpixel(G)
        #
        mon_image.putpixel(H, g)
        mon_image.putpixel(D, h)
        mon_image.putpixel(B, d)
        mon_image.putpixel(G, b)

    im2 = mon_image.copy()
    im2.save(f"image_de_test_10_{j:02}.ppm")

    return permute_tout(mon_image, j + 1)


fichier = "image_de_test_10.ppm"
im = Image.open(fichier)
permute_tout(im)
