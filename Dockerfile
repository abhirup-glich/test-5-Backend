FROM python:3.10-slim

# System deps for OpenCV-headless and general build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./requirements.txt
# Ensure CPU-only torch index is used and disable pip cache to reduce image size
ENV PIP_NO_CACHE_DIR=1
# Configure torch model cache inside container
ENV TORCH_HOME=/app/.cache/torch
RUN mkdir -p ${TORCH_HOME} && pip install -r requirements.txt

# Copy application code
COPY app ./app
COPY Logic ./Logic
COPY run.py ./run.py
COPY server.py ./server.py

# Pre-download and cache facenet_pytorch models (optional warmup)
# Comment out if you prefer downloading at first run to reduce image build time
RUN python - <<'PY'\n\
import os\n\
os.environ.setdefault('TORCH_HOME', '/app/.cache/torch')\n\
from facenet_pytorch import InceptionResnetV1, MTCNN\n\
# Instantiate to trigger weight downloads\n\
_ = InceptionResnetV1(pretrained='vggface2').eval()\n\
_ = MTCNN(keep_all=False)\n\
print('Model weights cached in', os.environ['TORCH_HOME'])\n\
PY

EXPOSE 5000

# Use gunicorn in production
CMD [\"gunicorn\", \"run:app\", \"-b\", \"0.0.0.0:5000\", \"--workers\", \"2\"]

