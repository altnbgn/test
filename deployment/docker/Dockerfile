# Building
FROM python:3.9.12-slim AS builder

RUN apt-get update && \
    apt-get install -y libpq-dev gcc ffmpeg libsm6 libxext6 libgl1

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt
# RUN pip install mmcv-full==1.7.0 -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.11.0/index.html
RUN mim install mmcv-full==1.7.0 
# RUN mim install "mmcv-full==1.6.2"
RUN mim install "mmdet==2.25.2"
RUN find /opt/venv \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+   

# Operation
FROM python:3.9.12-slim

RUN apt-get update && \
    apt-get install -y libpq-dev ffmpeg libsm6 libxext6 libgl1 -y && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONDONTWRITEBYCODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /code

COPY . /code/
COPY deployment/entrypoint.sh /entrypoint.sh
# CMD ["python", "main.py"]
ENTRYPOINT [ "/entrypoint.sh" ]