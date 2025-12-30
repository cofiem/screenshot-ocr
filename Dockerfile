FROM python:3.12@sha256:9465269ac36c61995cbbc722d1223b26cfa0ce9912bd1cd93fae0b161fcbb8c0

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
