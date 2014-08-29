
RUN = $$
WHICH = /usr/local/bin/$$
OLDWHICH = /usr/bin/$$

all:

install:
	ln -s $(CURDIR)/$(RUN) $(WHICH)

uninstall:
	rm $(WHICH)

olduninstall:
	rm $(OLDWHICH)

clean:
