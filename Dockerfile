FROM python:3.12@sha256:872565c5ac89cafbab19419c699d80bda96e9d0f47a4790e5229bd3aeeeb5da9

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install hatch click==8.2.2

COPY . .

RUN hatch run cov
