
# installation makefile for people willing to install locally
# ~/bin must be on the PATH

MAIN = $$
WHICH = ~/.bin/$$

install:
	ln -s $(CURDIR)/$(MAIN) $(WHICH)
	chmod a+x $(WHICH)

uninstall:
	rm $(WHICH)
