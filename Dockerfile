FROM python:3.12@sha256:21d856289d29a2d422292d45e33c8058a7eec64d889769123538e057621b3e52

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
