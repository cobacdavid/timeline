__author__ = "david cobac"
__date__ = 20201029


import os
import shutil
import subprocess
import sys
import json
import pyqrcode
import timeline_latexdef as tlLTX


fichier = sys.argv[1]
sortie = os.path.dirname(fichier)
base = os.path.basename(fichier)
nom_fichier = os.path.splitext(base)[0]

script_dir = os.path.dirname(sys.argv[0])
fichier_header = os.path.join(script_dir, "timeline_header.tex")
fichier_footer = os.path.join(script_dir, "timeline_footer.tex")

with open(fichier_header) as fh, open(fichier_footer) as ff:
    header = fh.read()
    footer = ff.read()


# lecture fichier source
with open(fichier) as fh:
    dico_tl = json.load(fh)

h, v, f, e = map(float,
                 [dico_tl["tailleH"],
                  dico_tl["tailleV"],
                  dico_tl["tailleFleche"],
                  dico_tl["espaceBloc"]])

# pour le nommage des qrcodes
nb_qrcode = 0

# écriture du fichier destination .tex
with open(os.path.join(sortie, f"{nom_fichier}_timeline.tex"), "w") as fh:
    fh.write(header)
    fh.write(tlLTX.chaine_definition_dim(h, v, f, e))
    #
    longueur = len(dico_tl["contenu"])
    commande = ["debut"] + ["milieu"] * (longueur - 2) + ["milieu"] # ["fin"]
    position = [0, 0]
    noeud = 0
    #
    for i in range(longueur):
        dico_element = dico_tl["contenu"][i]
        ##
        # les éléments par défaut
        trait = -5 if i % 2 else -2.5
        trait_v = 0
        if "trait" in dico_element:
            trait = float(dico_element["trait"])
            if trait > 0:
                trait += v
                trait_v = v
                #
        if "largeurCadre" in dico_element:
            largeurCadre = dico_element["largeurCadre"]
        else:
            largeurCadre = str(h)
            #
        if "couleur" in dico_element:
            couleurFond = dico_element["couleur"]
        else:
            couleurFond = "black!50"
            #
        if "couleurTitre" in dico_element:
            couleurTitre = dico_element["couleurTitre"]
        else:
            couleurTitre = "white"
        if "remplirCadre" in dico_element:
            remplirCadre = dico_element["remplirCadre"]
        else:
            remplirCadre = False
            ##
        centre_h = position[0] + h / 2
        #
        # la forme du timeline
        fh.write(tlLTX.bloc(commande[i], position, h, v, f, couleurFond))
        # le titre
        if i != 0:
            centre_h += f / 2
        fh.write(tlLTX.chaine_titre(centre_h, position[1] + v / 2,
                                    h,
                                    noeud,
                                    couleurTitre,
                                    dico_element["titre"]))
        noeud += 1
            # le cadre
        fh.write(tlLTX.cadre(centre_h, trait,
                             largeurCadre,
                             noeud,
                             dico_element["cadre"],
                             couleurFond,
                             remplirCadre))
        # la liaison
        if trait > 0:
            ancre = "south"
        else:
            ancre = "north"
        fh.write(tlLTX.liaison(f"{centre_h},{trait_v}",
                                   f"{noeud}.{ancre}",
                                   couleurFond))
        # traitement présence d'une image
        if 'imageCadre' in dico_element:
            dico_image = dico_element["imageCadre"]
            # valeurs par défaut
            if "xoffset" in dico_image:
                xoffset = dico_image["xoffset"]
            else:
                xoffset = dico_image["xoffset"]
                #
            if "yoffset" in dico_image:
                yoffset = dico_image["yoffset"]
            else:
                yoffset = "0"
                ##
            fh.write(tlLTX.image(dico_image["fichier"],
                                 noeud,
                                 dico_image["position"],
                                 dico_image["largeur"],
                                 xoffset,
                                 yoffset))
        # traitement qrcode
        if "url" in dico_element:
            url = dico_element["url"]
            nb_qrcode += 1
            qr = pyqrcode.create(url)
            nom_fichier = f"qrcode_{nb_qrcode}.png"
            qr.png(os.path.join(sortie, nom_fichier))
            #
            largeur_qr = min(h, float(largeurCadre))
            if trait > 0:
                ancre = "north"
                yoffset = str(largeur_qr / 2)
            else:
                ancre = "south"
                yoffset = str(-largeur_qr / 2)
                #
            fh.write(tlLTX.image(nom_fichier,
                                 noeud,
                                 ancre,
                                 str(largeur_qr),
                                 "0",
                                 yoffset))
            #
        noeud += 1
        position[0] += h + e
    fh.write(footer)

# Partie compilation
shutil.copyfile(os.path.join(script_dir, "Makefile"),
                os.path.join(sortie, "Makefile"))

rep_courant = os.getcwd()
if sortie == "":
    sortie = "."
os.chdir(sortie)
subprocess.call("make")
os.chdir(rep_courant)
