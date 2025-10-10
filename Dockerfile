FROM python:3.12@sha256:53724a5c8eb133046e0124fc2a623b00699949ecc475eb23daffdb547345bf86

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
