set shell := ["bash", "-c"]

mod docker '.just/docker.just'
mod lint '.just/lint.just'
mod tests '.just/test.just'
