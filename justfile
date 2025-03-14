set shell := ["bash", "-c"]

mod docker '.just/docker.just'
mod lint '.just/lint.just'
mod tests '.just/test.just'

[no-cd]
dev:
    uv pip install -e ".[dev]"
    pre-commit install
