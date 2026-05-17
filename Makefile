### Configure paths. ###
PROJECT_PATH := $(CURDIR)
ENV_PATH := $(CURDIR)/pyth_env
PYTHON := $(ENV_PATH)/bin/python3.11
TAG_NAME := DEPLOY
TAG_DATE := $(TAG_NAME)_$(shell date -u "+%Y_%m_%d_%H_%M_%S")

### Shell configure. ###
# For shell to bash to be able to use source.
SHELL = /bin/bash

# Shortcut to set env command before each python cmd.
VENV = source $(ENV_PATH)/bin/activate

# Config is based on two environment files, initalized here.
virtualenv: $(ENV_PATH)/bin/activate

$(ENV_PATH)/bin/activate:
	virtualenv -p /usr/bin/python3.11 $(ENV_PATH)

### Manage project installation. ###
# Install python requirements.
pip: virtualenv
	$(VENV) && cd $(CURDIR) && pip3 install -r $(CURDIR)/requirements.txt;

clean:
	find . -name '*.pyc' -delete

diff_filters:
	$(VENV) && python3 filters.py
	
verify_filter:
	$(VENV) && python3 verify_filter.py

cuenca_birds:
	$(VENV) && python3 cuenca_birds.py

lista_guia_uda:
	$(VENV) && python3 diff_guide_ebird.py --guide guia_uda
	@echo "=> lista_guia_uda.html"

lista_ucuenca:
	$(VENV) && python3 diff_guide_ebird.py --guide ucuenca
	@echo "=> lista_ucuenca.html"

lista_cajas:
	$(VENV) && python3 diff_guide_ebird.py --guide cajas
	@echo "=> lista_cajas.html"

cuenca_migratorias:
	$(VENV) && python3 migratorias.py
	@echo "=> migratorias.html"

bird_list_ecuador:
	$(VENV) && python3 bird_list_ecuador.py

deploy: lista_ucuenca lista_guia_uda lista_cajas cuenca_migratorias
	scp -r dist/* guiguide@ssh-guiguide.alwaysdata.net:/home/guiguide/www/cuenca_birds/
	git tag $(TAG_DATE); git push origin $(TAG_DATE) --no-verify