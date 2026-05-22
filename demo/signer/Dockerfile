FROM python:3.11-slim
WORKDIR /workspace

# system deps for pillow/fitz if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# copy workspace (read-only preferred when mounted)
COPY . /workspace

RUN python -m pip install --upgrade pip
RUN pip install -r /workspace/backend/requirements.txt || true
RUN pip install -r /workspace/Coding/requirements.txt || true

ENV PYTHONPATH=/workspace

CMD ["/bin/sh", "-c", "python /workspace/scripts/batch_sign.py --csv /workspace/tests/fixtures/sample_batch.csv --out /artifacts/sample_signed.zip --gen-key-out /artifacts/ci_key.b64"]
