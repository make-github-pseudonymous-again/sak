
RUN = run.py
WHICH = /usr/bin/p

all:

install:
	ln -s $(CURDIR)/$(RUN) $(WHICH)

uninstall:
	rm $(WHICH)

clean: