FROM python:3.12@sha256:2b075cba87fcf51f14e6be18f83f209fb2013d72362ec874aed7d01933253e8b

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
