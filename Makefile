
RUN = run.py
WHICH = /usr/bin/$$

all:

install:
	ln -s $(CURDIR)/$(RUN) $(WHICH)

uninstall:
	rm $(WHICH)

clean:
