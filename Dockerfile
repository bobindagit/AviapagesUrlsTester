FROM python:3.10.0
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /working/sitemap_tester

COPY requirements.txt /working/sitemap_tester/
RUN pip install --no-cache-dir -r /working/sitemap_tester/requirements.txt

COPY . /working/sitemap_tester

ENV SITEMAP_LINK="https://aviapages.com/sitemap.xml"
ENV RETRIES_COUNT=3

CMD ["python", "-u", "main.py"]