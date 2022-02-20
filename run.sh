#!/bin/bash

LOCAL_PATH="/users/vladimirmelnic"

docker build --tag sitemap_tester .
docker run -it --name sitemap_tester sitemap_tester
docker cp sitemap_tester:/working/sitemap_tester/report.csv $LOCAL_PATH
docker rm sitemap_tester