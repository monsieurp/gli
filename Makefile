PROGNAME= gli
VERSION=  0.1
PREFIX=   /usr/share/$(PROGNAME)-$(VERSION)

.PHONY: install
install: gli
	mkdir -p $(DESTDIR)$(PREFIX)
	$(foreach script, $(wildcard ./scripts/*), \
		install -m 755 $(script) $(DESTDIR)$(PREFIX) \
	;)
	install -m 755 $< $(DESTDIR)/usr/bin

.PHONY: uninstall
uninstall: gli
	rm -rvf $(DESTDIR)$(PREFIX)
	rm -vf $(DESTDIR)/usr/bin/$<
