.PHONY : new_venv init install checker

new_venv:
	@python3.7 -mvenv venv

init: new_venv
	@source venv/bin/activate; pip install --upgrade pip
	$(MAKE) install

install:
	@source venv/bin/activate; pip install -e .

checker:
	$(MAKE) -C porcupine
	mkdir -p bin
	cp porcupine/bin/bank bin/checker-bank
