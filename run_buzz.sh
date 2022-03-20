#!/bin/bash

docker-compose --file "docker-compose_buzz.yml" --env-file "var.env" --project-name sitemap_tester_buzz build
docker-compose --file "docker-compose_buzz.yml" --env-file "var.env" --project-name sitemap_tester_buzz run python_app
docker-compose --file "docker-compose_buzz.yml" --env-file "var.env" --project-name sitemap_tester_buzz stop python_app
docker container stop sitemap_tester_buzz-redis-1
docker container prune -f
docker image prune -f
docker volume prune -f