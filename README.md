# Timeline

Produit un timeline à partir d'un json

## Flux

.json --python-->( .tex --(LuaLaTeX)--> ).pdf

## Utiliser
`python3 timeline.py mon/super/chemin/vers/monFichier.json`

Création de 2 fichiers : un `Makefile` et
`monFichier_timeline.pdf`, le tout dans le répertoire du fichier
json initial.

## Requis 

* [lib python  PyQRCode](https://pypi.org/project/PyQRCode/) + [lib python pypng](https://pypi.org/project/pypng/)
* [LuaLaTex](http://luatex.org/) + [TikZ](https://www.ctan.org/pkg/pgf)


## json

Quatre variables (type chaîne) `largeurBloc`, `hauteurBloc`,
`largeurFleche` et `espaceInterBloc` pour l'apparence des blocs.

Une variable (type liste) `contenu` de dictionnaires, chaque
élément de laiste décrit les blocs consécutivement.  Un
dictionnaire peut-être vide (bloc construit par défaut) ou peut
contenir une ou plusieurs de ces clés (pour des valeurs type chaîne
ou booléen, valeurs par défaut entre parenthèses) :

* `couleurFond` : couleur TikZ à utiliser pour ce bloc (`black!50`)
* `texteTitre` : texte du bloc en LaTeX avec backslahs échappés (double-backslash) (vide)
* `texteCadre` : texte de l'encadré (idem) (vide)
* `largeurCadre` et `hauteurCadre` : dimensions en cm sans l'unité (largeur et hauteur d'un bloc par défaut)
* `remplirCadre` : booléen JS (true ou false) de remplissage du cadre (`false`)
* `hauteurTrait` : hauteur de la liaison bloc-cadre, négatif vers
  le bas et positif vers le haut (`-5` alternant avec `-2.5`) 
* `url` : url transformé en QRCode au-dessus ou en-dessous du cadre (vide)
* `imageCadre` : dictionnaire d'intégration d'une image près de l'encadré (vide)
     * `fichier` : fichier image (vide mais obligatoire)
     * `largeur` : largeur demandée (.25 de la largeur de l'encadré)
     * `position` : position relative TikZ : north, south, west,
     east, south west ... (`east`)
     * `xoffset` : décalage horizontal / position relative (`0`)
     * `yoffset` : décalage vertical / position relative (`0`)

Voici les premières lignes du fichier exemple [`timeline_internet.json`](./exemples/internet/timeline_internet.json)

``` javascript
{
    "largeurBloc":     "2",
    "hauteurBloc":     "1",
    "largeurFleche":   "0.5",
    "espaceInterBloc": "0.1",
    "contenu": [
        {
            "texteTitre":   "1968",
            "texteCadre":   "\\textbf{Naissance d'ARPANET}  (DoD)",
            "hauteurTrait": "1",
            "largeurCadre": "4",
            "remplirCadre": true,
            "couleurFond":  "pink!60"
        },
        {
            "texteTitre":   "1969",
            "texteCadre":   "1\\iere{} connexion\\\\L.A./Stanford",
            "largeurCadre": "2.5",
            "couleurFond":  "pink!60"
        },
        {
            "texteTitre":   "1971",
        ...
        ... 
```

## Licence
CC-BY-NC-SA
