FROM python:3.12@sha256:3466e9a530f0226fc09fbc479bde2387fd773f760749612e94d8696fe1aa5877

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
