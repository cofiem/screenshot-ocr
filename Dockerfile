FROM python:3.12@sha256:746223db759d2cbbde1e066cb49126f460bce66d22147e540ba604438d2296ed

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
