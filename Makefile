TEX_SRC    = $(wildcard *.tex)
# Commandes
LUALATEX   = lualatex
OPT_LUALATEX = --shell-escape --interaction=batchmode
# 
PDF        = $(TEX_SRC:%.tex=%.pdf)
# 
TO_DEL_C   = *.aux *.log *.toc *.lof *.lot *.mpx *.tmp  *.tex qrcode_* *~
#
all: $(PDF) clean

clean:
	@rm -f $(TO_DEL_C)
# pdf
%.pdf: %.tex
	@$(LUALATEX) $(OPT_LUALATEX) $< 2>/dev/null 1>&2

