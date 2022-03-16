#!/bin/bash

docker build --file "Dockerfile_tests" --tag sitemap_tester_tests .
docker run -it --name sitemap_tester_tests --env-file "var.env" sitemap_tester_tests
docker container prune -f
docker image prune -f