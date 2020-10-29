__author__ = "david cobac"
__date__ = 20201029


import os
import sys
import json
import pyqrcode


fichier = sys.argv[1]
sortie = os.path.dirname(fichier)
base = os.path.basename(fichier)
nom_fichier = os.path.splitext(base)[0]

fichier_header = "timeline_header.tex"
fichier_footer = "timeline_footer.tex"
with open(fichier_header) as fh, open(fichier_footer) as ff:
    header = fh.read()
    footer = ff.read()


def chaine_definition_dim(h, v, f, e):
    s = "\n"
    for valeur, variable in zip([h, v, f, e],
                                [r"\tailleH", r"\tailleV",
                                 r"\tailleFleche", r"\espaceBloc"]):
        s += r"\pgfmathsetmacro{" + variable + "}{" + f"{valeur}" + "}\n"
    return s


def chaine_titre(x, y, largeur, i, couleurTexte, titre):
    s = fr"\node ({i}) at ({x},{y})"
    s += r" {\begin{minipage}{" + str(largeur) + "cm}\n"
    s += r"\begin{center}" + "\n"
    s += r"\bfseries \Large \textcolor{" + couleurTexte + "}"
    s += "{" + titre + "}" + "\n"
    s += r"\end{center}"
    s += r"\end{minipage}};" + "\n"
    return s


def cadre(x, y, largeur, noeud, texte, couleur, remplir):
    remplissage = f"fill={couleur}," if remplir else ""
    s = fr"\node[draw={couleur}," + remplissage +\
        "radius=5pt,rounded corners,line width=1bp]" + "\n"
    s += f"({noeud}) at ({x},{y})"
    s += r" {\begin{minipage}{" + largeur + "cm}" + "\n"
    s += texte + "\n"
    s += r"\end{minipage}};" + "\n"
    return s


def image(fichier, noeud, position, largeur, xoff, yoff):
    s = r"\node[inner sep=0pt,xshift=" + xoff + "cm, yshift=" + yoff + "cm] "
    s += "(" + fichier.split(".")[0] + ")"
    s += " at (" + str(noeud) + "." + position + ")"
    s += r"{\includegraphics[width=" + largeur + "cm]{" + fichier + "}};\n"
    return s


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
with open(f"{nom_fichier}_timeline.tex", "w") as fh:
    fh.write(header)
    fh.write(chaine_definition_dim(h, v, f, e))
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
        fh.write(fr"\{commande[i]}"
                 + f"(({position[0]},{position[1]}),{h},{v},{f},{couleurFond})"
                 + "\n")
        # le titre
        if i != 0:
            centre_h += f / 2
        fh.write(chaine_titre(centre_h, position[1] + v / 2,
                              h,
                              noeud,
                              couleurTitre,
                              dico_element["titre"]))
        noeud += 1
        # le cadre
        fh.write(cadre(centre_h, trait,
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
        fh.write(r"\draw[line width=2mm," + couleurFond
                 + f"] ({centre_h},{trait_v})--({noeud}.{ancre});"
                 + "\n")
        #
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
            fh.write(image(dico_image["fichier"],
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
            nom_fichier = os.path.join(sortie, f"qrcode_{nb_qrcode}.png")
            qr.png(nom_fichier)
            #
            largeur_qr = min(h, float(largeurCadre))
            if trait > 0:
                ancre = "north"
                yoffset = str(largeur_qr / 2)
            else:
                ancre = "south"
                yoffset = str(-largeur_qr / 2)
            #
            fh.write(image(nom_fichier,
                           noeud,
                           ancre,
                           str(largeur_qr),
                           "0",
                           yoffset))
        #
        noeud += 1
        position[0] += h + e
    fh.write(footer)
