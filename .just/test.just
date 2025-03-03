set shell := ["bash", "-c"]

[no-cd]
e2e:
    sudo docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
