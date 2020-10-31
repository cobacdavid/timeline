def chaine_definition_dim(h, v, f, e):
    s = "\n"
    for valeur, variable in zip([h, v, f, e],
                                [r"\tailleH", r"\tailleV",
                                 r"\tailleFleche", r"\espaceBloc"]):
        s += r"\pgfmathsetmacro{" + variable + "}{" + f"{valeur}" + "}\n"
    return s


def bloc(commande, position, h, v, f, dico_valeurs):
    couleur_fond = dico_valeurs["couleurFond"]
    s = fr"\{commande}"
    s += f"(({position[0]},{position[1]}),{h},{v},{f},{couleur_fond})" + "\n"
    return s


def chaine_titre(x, y, largeur, i, dico_valeurs):
    couleur_texte = dico_valeurs["couleurTitre"]
    titre = dico_valeurs["texteTitre"]
    #
    s = fr"\node ({i}) at ({x},{y})"
    s += r" {\begin{minipage}{" + str(largeur) + "cm}\n"
    s += r"\begin{center}" + "\n"
    s += r"\bfseries \Large \textcolor{" + couleur_texte + "}"
    s += "{" + titre + "}" + "\n"
    s += r"\end{center}"
    s += r"\end{minipage}};" + "\n"
    return s


def cadre(x, y, noeud, dico_valeurs):
    largeur = dico_valeurs["largeurCadre"]
    hauteur = dico_valeurs["hauteurCadre"]
    texte = dico_valeurs["texteCadre"]
    couleur = dico_valeurs["couleurFond"]
    remplissage = f"fill={couleur}," if dico_valeurs["remplirCadre"] else ""
    #
    w_min_size = f"minimum width={largeur}cm," if texte == "" else ""
    h_min_size = f"minimum height={hauteur}cm," if texte == "" else ""
    #
    s = fr"\node[draw={couleur}," + remplissage +\
        f"{w_min_size}{h_min_size}radius=5pt,rounded corners,line width=1bp]" + "\n"
    s += f"({noeud}) at ({x},{y})"
    s += r" {\begin{minipage}{" + largeur + "cm}" + "\n"
    s += texte + "\n"
    s += r"\end{minipage}};" + "\n"
    return s


def liaison(de, vers, dico_valeurs):
    couleur = dico_valeurs["couleurFond"]
    #
    s = r"\draw[line width=2mm," + couleur + "]"
    s += f"({de})--({vers});" + "\n"
    return s


def image(fichier, noeud, position, largeur, xoff, yoff):
    s = r"\node[inner sep=0pt,xshift=" + xoff + "cm, yshift=" + yoff + "cm] "
    s += "(" + fichier.split(".")[0] + ")"
    s += " at (" + str(noeud) + "." + position + ")"
    s += r"{\includegraphics[width=" + largeur + "cm]{" + fichier + "}};\n"
    return s
