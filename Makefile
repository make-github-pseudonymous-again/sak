
MAIN = sak
WHICH = /usr/local/bin/$$
OLDWHICH = /usr/bin/$$

all:

install:
	ln -s $(CURDIR)/$(MAIN) $(WHICH)
	chmod a+x $(WHICH)

uninstall:
	rm $(WHICH)

olduninstall:
	rm $(OLDWHICH)

clean:
