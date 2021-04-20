__author__ = "david cobac"
__date__ = 20201029
__last_modified__ = 20210420


import os
import shutil
import subprocess
import sys
import json
import pyqrcode
import timeline_latexdef as tlLTX


fichier_source = sys.argv[1]

dir_sortie = os.path.dirname(fichier_source)
if dir_sortie == "":
    dir_sortie = "."
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
    dico_json = json.load(fh)

# distances globales externes
dim_globales_defaut = {
    "largeurBloc": 4,
    "hauteurBloc": 2,
    "largeurFleche": .5,
    "espaceInterBloc": 0.1
}
dim_globales = dim_globales_defaut.copy()
for k in dico_json:
    if k != "contenu" and k != "codeComplement"\
       and k != "toutBloc" and k != "touteImage":
        dim_globales[k] = float(dico_json[k])

if "incrementBloc" not in dico_json:
    dim_globales["incrementBloc"] = dim_globales["largeurBloc"]

# pour le nommage des qrcodes
nb_qrcode = 0

# écriture du fichier destination .tex
with open(os.path.join(dir_sortie, f"{nom_fichier}_timeline.tex"), "w") as fh:
    fh.write(header)
    #
    # code Tikz / LaTeX à insérer
    if "codeComplement" in dico_json:
        for code in dico_json["codeComplement"]:
            fh.write(code + "\n")
            #
            #
    longueur = len(dico_json["contenu"])
    position = [0, 0]
    noeud = 0
    # valeurs par défaut script
    valeurs_par_defaut_script = {
        "couleurFond": "black!50",
        "couleurTitre": "white",
        "largeurBloc": str(dim_globales["largeurBloc"]),
        "remplirBloc": False,
        "texteTitre": "",
        "largeurCadre": str(dim_globales["largeurBloc"]),
        "hauteurCadre": str(dim_globales["hauteurBloc"]),
        "remplirCadre": False,
        "positionCadre": "dessous", # "dessus" ou "double"
        "hauteurTrait": 5,
        "texteCadre": "",
        "xoffset": "0",
        "yoffset": "0"
    }
    # valeurs par défaut utilisateur
    valeurs_par_defaut = valeurs_par_defaut_script.copy()
    if "toutBloc" in dico_json:
        for k in dico_json["toutBloc"]:
            valeurs_par_defaut[k] = dico_json["toutBloc"][k]
    #
    # images : valeur par défaut script
    images_valeurs_par_defaut_script = {
        "xoffset": "0",
        "yoffset": "0",
        "position": "east"
    }
    # images : valeur par défaut utilisateur
    images_valeurs_par_defaut = images_valeurs_par_defaut_script.copy()
    if "touteImage" in dico_json:
        for k in dico_json["touteImage"]:
            images_valeurs_par_defaut[k] = dico_json["touteImage"][k]
    #
    #
    for i in range(longueur):
        dico_element = dico_json["contenu"][i]
        #
        valeurs = valeurs_par_defaut.copy()
        #
        #
        if type(valeurs["hauteurTrait"]) == list:
            v_hT = valeurs["hauteurTrait"][i % len(valeurs["hauteurTrait"])]
        else:
            v_hT = valeurs["hauteurTrait"]
        #
        if "formeBloc" not in valeurs_par_defaut:
            if i == 0:
                valeurs["formeBloc"] = "debut"
            elif i == longueur - 1:
                valeurs["formeBloc"] = "fin"
            else:
                valeurs["formeBloc"] = "milieu"
        # valeurs à transformer selon le bloc particulier
        for k in valeurs:
            valeurs[k] = dico_element.get(k, valeurs[k])
        #
        # trait est à traiter à part... compte tenu de sa valeur
        # par défaut.
        depart_trait_dessous = float(valeurs["yoffset"])
        arrivee_trait_dessous = depart_trait_dessous - float(v_hT) \
            - dim_globales["hauteurBloc"]
        #
        depart_trait_dessus = float(valeurs["yoffset"]) + dim_globales["hauteurBloc"]
        arrivee_trait_dessus = depart_trait_dessus + float(v_hT) \
            + dim_globales["hauteurBloc"]
        #
        #
        centre_h = position[0] +\
            float(valeurs["xoffset"]) +\
            float(valeurs["largeurBloc"]) / 2
        #
        # BLOC DE TITRE
        fh.write(tlLTX.bloc((position[0] + float(valeurs["xoffset"]),
                             position[1] + float(valeurs["yoffset"])),
                            dim_globales, valeurs))
        # le titre
        if i != 0:
            centre_h += dim_globales["largeurFleche"] / 2
        fh.write(tlLTX.chaine_titre(centre_h,
                                    position[1]
                                    + float(valeurs["yoffset"])
                                    + dim_globales["hauteurBloc"] / 2,
                                    dim_globales["largeurBloc"],
                                    noeud,
                                    valeurs))
        noeud += 1
        # CADRE
        if valeurs["positionCadre"] == "dessus":
            fh.write(tlLTX.cadre(centre_h, arrivee_trait_dessus, noeud, valeurs))
            fh.write(tlLTX.liaison(f"{centre_h},{depart_trait_dessus}",
                                   f"{noeud}.south", valeurs))
        elif valeurs["positionCadre"] == "dessous":
            fh.write(tlLTX.cadre(centre_h, arrivee_trait_dessous, noeud, valeurs))
            fh.write(tlLTX.liaison(f"{centre_h},{depart_trait_dessous}",
                                   f"{noeud}.north", valeurs))
        elif valeurs["positionCadre"] == "double":
            fh.write(tlLTX.cadre(centre_h, arrivee_trait_dessus, noeud, valeurs))
            fh.write(tlLTX.liaison(f"{centre_h},{depart_trait_dessus}",
                                   f"{noeud}.south", valeurs))
            noeud += 1
            fh.write(tlLTX.cadre(centre_h, arrivee_trait_dessous, noeud, valeurs))
            fh.write(tlLTX.liaison(f"{centre_h},{depart_trait_dessous}",
                                   f"{noeud}.north", valeurs))
        else:
            pass
        #
        # IMAGE
        if 'imageCadre' in dico_element:
            dico_image = dico_element["imageCadre"]
            #
            # valeur par défaut dynamiques si elle n'existe pas
            # chez les valeurs par défaut utilisateur
            if "largeur" not in images_valeurs_par_defaut:
                images_valeurs_par_defaut["largeur"] = \
                    str(.25 * float(valeurs["largeurCadre"]))
            # application valeurs individuelles
            images_valeurs = images_valeurs_par_defaut.copy()
            for k in dico_image:
                images_valeurs[k] = dico_image[k]
            ##
            fh.write(tlLTX.image(images_valeurs, noeud))
            #
        # traitement QRCODE
        if "url" in dico_element:
            url = dico_element["url"]
            nb_qrcode += 1
            qr = pyqrcode.create(url, error='L')
            nom_fichier = f"qrcode_{nb_qrcode}.png"
            qr.png(os.path.join(dir_sortie, nom_fichier))
            #
            largeur_qr = min(dim_globales["hauteurBloc"],
                             float(valeurs["largeurCadre"]))
            if arrivee_trait > 0:
                ancre = "north"
                yoffset = str(largeur_qr / 2)
            else:
                ancre = "south"
                yoffset = str(-largeur_qr / 2)
            #
            dico_image_url = {
                "fichier": nom_fichier,
                "position": ancre,
                "xoffset": "0",
                "yoffset": yoffset,
                "largeur": str(largeur_qr)
            }
            fh.write(tlLTX.image(dico_image_url, noeud))
            #
        noeud += 1
        #
        # fh.write(r"\draw (current bounding box.north west) --
        # (current bounding box.south east);")
        #
        increment = dim_globales["incrementBloc"]
        if "largeurBloc" in dico_element:
            increment = float(valeurs["largeurBloc"])
        position[0] += increment + dim_globales["espaceInterBloc"]
    fh.write(footer)

# Partie compilation
shutil.copyfile(os.path.join(dir_script, "Makefile"),
                os.path.join(dir_sortie, "Makefile"))

rep_courant = os.getcwd()
os.chdir(dir_sortie)
subprocess.call("make")
os.chdir(rep_courant)
