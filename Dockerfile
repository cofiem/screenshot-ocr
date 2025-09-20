FROM python:3.12

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
