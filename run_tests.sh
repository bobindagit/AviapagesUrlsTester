#!/bin/bash

docker-compose --file "docker-compose_tests.yml" --env-file "var.env" --project-name sitemap_tester_tests build
docker-compose --file "docker-compose_tests.yml" --env-file "var.env" --project-name sitemap_tester_tests run python_app
docker-compose --file "docker-compose_tests.yml" --env-file "var.env" --project-name sitemap_tester_tests stop python_app
docker container stop sitemap_tester_tests-redis-1
docker container prune -f
docker image prune -f
docker volume prune -f