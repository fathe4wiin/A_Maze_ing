PYTHON = python3
PIP = pip3

MAIN = mymaze/a_maze_ing.py

.PHONY: all install run debug clean lint

all: run

install:
	$(PIP) install mlx-2.2-py3-none-manylinux1_x86_64.whl

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
