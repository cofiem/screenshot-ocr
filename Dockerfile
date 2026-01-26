FROM python:3.14@sha256:17bc9f1d032a760546802cc4e406401eb5fe99dbcb4602c91628e73672fa749c

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
