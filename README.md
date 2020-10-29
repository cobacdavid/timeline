# Timeline

Produit un timeline à partir d'un json

## Flux

.json --(LuaLaTeX)--> .tex --> .pdf

## Aide
1. Voir le .json exemple
2. exécuter `python3 timeline.py monFichier.json`
3. exécuter `lualatex --shell-escape monFichier_timeline.tex`

## Requis
1. [lib python  PyQRCode](https://pypi.org/project/PyQRCode/) + [lib python pypng](https://pypi.org/project/pypng/)
2. [LuaLaTex](http://luatex.org/) + [TikZ](https://www.ctan.org/pkg/pgf)

## Licence
CC-BY-NC-SA
