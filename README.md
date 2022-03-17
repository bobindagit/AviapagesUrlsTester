## AviaPages SITEMAP Tester

# REQUIREMENTS (python packages)
* requests==2.27.1
* beautifulsoup4==4.10.0
* random-user-agent==1.0.1
* alive_progress==2.3.1
* lxml==4.8.0
* redis==4.1.4
* aioredis==2.0.1
* hiredis==2.0.0
* nltk==3.7
* contractions==0.1.66
* aiohttp==3.8.1
* aiofiles==0.8.0

# HOW TO USE
1. First you need to install Docker and Docker-compose to deploy application.
2. Set up ENV variables in the var.env file.
> RETRIES_COUNT - urls check count
> 
> MIN_WORDS_COUNT - minimum pass gate number of words for report
>
> ANALYZE_SEO_BUZZ - 1 or 0 - additional SEO analyze for buzz links
> 
> NUM_CORES - cpu cores count
> 
> LOCAL_PATH - local path for saving reports
4. Run script
> run_main.sh - test main sitemap urls
> 
> run_buzz.sh - test buzz urls, analyze titles and article bodies words
> 
> run_tests.sh - unit testing