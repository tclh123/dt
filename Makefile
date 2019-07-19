.PHONY : new_venv init install freeze web tail web-stop

new_venv:
	@python3.7 -mvenv venv

init: new_venv
	@source venv/bin/activate; pip install --upgrade pip
	$(MAKE) install

install:
	@source venv/bin/activate; pip install -e .

web: web-stop
	@mkdir -p tmp
	@echo redirect log to tmp/dev.log
	@source venv/bin/activate; gunicorn -w 4 -k uvicorn.workers.UvicornWorker --log-level debug -b 0.0.0.0:8123 --limit-request-line 0 --limit-request-fields 32767 --limit-request-field_size 0 app:app >tmp/dev.log 2>&1 &

tail:
	@tail -F tmp/dev.log

web-stop:
	@lsof -i :8123 | awk '{print $$2}'| uniq | tail -n+2 | xargs --no-run-if-empty kill
	@sleep 1
