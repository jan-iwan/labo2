PYTHON = python3.11
PYFLAGS =
SCRIPTS = resonancia amplitud distancia

PYCACHE = $(shell find '.' -name '__pycache__')

all: $(SCRIPTS)

$(SCRIPTS):
	$(PYTHON) ./main.py $(PYFLAGS) $@

clean:
	rm -rf $(PYCACHE)
