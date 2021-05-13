.PHONY: run
run:
	@. env/bin/activate && . environment.sh && cd src && python app.py

.PHONY: install
install:
	@cd deployment && bash install.sh
