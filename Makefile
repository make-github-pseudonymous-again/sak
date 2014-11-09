
MAIN = main.py
WHICH = /usr/local/bin/$$
OLDWHICH = /usr/bin/$$

all:

install:
	ln -s $(CURDIR)/$(MAIN) $(WHICH)

uninstall:
	rm $(WHICH)

olduninstall:
	rm $(OLDWHICH)

clean:
