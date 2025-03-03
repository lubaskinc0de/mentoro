set shell := ["bash", "-c"]

[no-cd]
up:
    sudo docker compose up --build

[no-cd]
down:
    sudo docker compose down
    sudo docker compose -f docker-compose.test.yml down

[no-cd]
clear:
    sudo docker compose down -v
