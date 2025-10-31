FROM python:3.12@sha256:72e5baf244fb1a9ddc985800340b48c2a0c72fdc9479e95d0f39987284f9f1cd

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
