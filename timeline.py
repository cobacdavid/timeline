__author__ = "david cobac"
__date__ = 20201029


import os
import shutil
import subprocess
import sys
import json
import pyqrcode
import timeline_latexdef as tlLTX


fichier_source = sys.argv[1]
dir_sortie = os.path.dirname(fichier_source)
fichier_basename = os.path.basename(fichier_source)
nom_fichier = os.path.splitext(fichier_basename)[0]

dir_script = os.path.dirname(sys.argv[0])
fichier_header = os.path.join(dir_script, "timeline_header.tex")
fichier_footer = os.path.join(dir_script, "timeline_footer.tex")

with open(fichier_header) as fh, open(fichier_footer) as ff:
    header = fh.read()
    footer = ff.read()


# lecture fichier source json
with open(fichier_source) as fh:
    dico_tl = json.load(fh)

# distances globales
h, v, f, e = map(float,
                 [dico_tl["largeurBloc"],
                  dico_tl["hauteurBloc"],
                  dico_tl["largeurFleche"],
                  dico_tl["espaceInterBloc"]])

# pour le nommage des qrcodes
nb_qrcode = 0

# écriture du fichier destination .tex
with open(os.path.join(dir_sortie, f"{nom_fichier}_timeline.tex"), "w") as fh:
    fh.write(header)
    fh.write(tlLTX.chaine_definition_dim(h, v, f, e))
    #
    longueur = len(dico_tl["contenu"])
    # fin permet d'avoir un bloc fermé en dernier bloc
    # 3 possibilités : "debut", "milieu" ou "fin"
    # on ne laisse pas le choix... à voir
    commande = ["debut"] + ["milieu"] * (longueur - 2) + ["milieu"]
    position = [0, 0]
    noeud = 0
    #
    valeurs_par_defaut = {"couleurFond": "black!50",
                          "couleurTitre": "white",
                          "texteTitre": "",
                          "largeurCadre": str(h),
                          "hauteurCadre": str(v),
                          "remplirCadre": False,
                          "texteCadre": ""}

    for i in range(longueur):
        dico_element = dico_tl["contenu"][i]
        #
        valeurs_par_defaut["hauteurTrait"] = -5 if i % 2 else -2.5
        valeurs = valeurs_par_defaut.copy()
        for k in valeurs_par_defaut:
            valeurs[k] = dico_element.get(k, valeurs[k])
        #
        # trait est à traiter à part... compte tenu de sa valeur
        # par défaut.
        depart_trait = 0
        arrivee_trait = float(valeurs["hauteurTrait"])
        ancre = "north"
        if arrivee_trait > 0:
            # on oriente le trait vers le haut
            # du coup ça change l'ancrage en destination
            # et le point de départ aussi
            arrivee_trait += v
            depart_trait = v
        #
        centre_h = position[0] + h / 2
        #
        # la forme du timeline
        fh.write(tlLTX.bloc(commande[i], position, h, v, f, valeurs))
        # le titre
        if i != 0:
            centre_h += f / 2
        fh.write(tlLTX.chaine_titre(centre_h, position[1] + v / 2,
                                    h,
                                    noeud,
                                    valeurs))
        noeud += 1
        # le cadre
        fh.write(tlLTX.cadre(centre_h, arrivee_trait, noeud, valeurs))
        # la liaison
        if arrivee_trait > 0:
            ancre = "south"
        else:
            ancre = "north"
        fh.write(tlLTX.liaison(f"{centre_h},{depart_trait}",
                                   f"{noeud}.{ancre}", valeurs))
        # traitement présence d'une image
        if 'imageCadre' in dico_element:
            dico_image = dico_element["imageCadre"]
            # valeurs par défaut
            if "xoffset" in dico_image:
                xoffset = dico_image["xoffset"]
            else:
                xoffset = "0"
            #
            if "yoffset" in dico_image:
                yoffset = dico_image["yoffset"]
            else:
                yoffset = "0"
            #
            if "largeur" in dico_image:
                image_largeur = dico_image["largeur"]
            else:
                image_largeur = str(.25 * float(valeurs["largeurCadre"]))
            #
            if "position" in dico_image:
                image_position = dico_image["position"]
            else:
                image_position = "east"
            ##
            fh.write(tlLTX.image(dico_image["fichier"], noeud,
                                 image_position, image_largeur,
                                 xoffset, yoffset))
        # traitement qrcode
        if "url" in dico_element:
            url = dico_element["url"]
            nb_qrcode += 1
            qr = pyqrcode.create(url, error='L')
            nom_fichier = f"qrcode_{nb_qrcode}.png"
            qr.png(os.path.join(dir_sortie, nom_fichier))
            #
            largeur_qr = min(h, float(valeurs["largeurCadre"]))
            if arrivee_trait > 0:
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
shutil.copyfile(os.path.join(dir_script, "Makefile"),
                os.path.join(dir_sortie, "Makefile"))

rep_courant = os.getcwd()
if dir_sortie == "":
    dir_sortie = "."
os.chdir(dir_sortie)
subprocess.call("make")
os.chdir(rep_courant)
