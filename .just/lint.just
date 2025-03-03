set shell := ["bash", "-c"]

[no-cd]
run:
    ruff check --fix
    ruff format
    mypy
