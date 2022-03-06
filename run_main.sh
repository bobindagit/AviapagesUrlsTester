#!/bin/bash

LOCAL_PATH="/users/vladimirmelnic/reports"

docker build --file "Dockerfile_main" --tag sitemap_tester_main .
docker run -it --name sitemap_tester_main --env-file "env.dev" sitemap_tester_main
docker cp sitemap_tester_main:/working/sitemap_tester/reports/report_main.csv $LOCAL_PATH
docker container prune -f
docker image prune -f