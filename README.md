# Timeline

Produit un timeline à partir d'un json

## Flux

.json --(python)--> .tex --(LuaLaTeX)--> .pdf

## Aide
1. Voir le .json exemple
2. `python3 timeline.py mon/super/chemin/vers/monFichier.json`
3. création de 2 fichiers : `Makefile` et `mon/super/chemin/vers/monFichier_timeline.pdf`

## Requis
1. [lib python  PyQRCode](https://pypi.org/project/PyQRCode/) + [lib python pypng](https://pypi.org/project/pypng/)
2. [LuaLaTex](http://luatex.org/) + [TikZ](https://www.ctan.org/pkg/pgf)

## Licence
CC-BY-NC-SA
