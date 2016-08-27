TARGET=report

all: $(TARGET).pdf

$(TARGET).pdf: $(TARGET).tex
	pdflatex $(TARGET).tex -interaction=nonstopmode -halt-on-error
	bibtex $(TARGET)
	pdflatex $(TARGET).tex -interaction=nonstopmode -halt-on-error
	pdflatex $(TARGET).tex -interaction=nonstopmode -halt-on-error

clean:
	rm -f $(TARGET).pdf $(TARGET).aux $(TARGET).bbl $(TARGET).blg $(TARGET).log$(TARGET).pdf
