.PHONY: install run debug clean lint lint-strict

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e .
	.venv/bin/pip install mlx-2.2-py3-none-manylinux1_x86_64.whl
	.venv/bin/pip install flake8 mypy

run:
	. .venv/bin/activate && python3 main.py config.txt

debug:
	.venv/bin/python -m pdb main.py

clean:
	rm -rf **/__pycache__ **/.mypy_cache **/*.egg-info **/*.pyc **/*.pyo 2>/dev/null || true

lint:
	flake8 setup.py main.py MazeGenlib/
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 setup.py main.py MazeGenlib/
	mypy . --strict
