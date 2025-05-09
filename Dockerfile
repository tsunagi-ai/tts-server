FROM python:3.10-slim

WORKDIR /

# Pre-install system dependencies separately to leverage Docker cache
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

COPY model_config.py /
COPY rp_handler.py /
COPY model_cacher.py /

# Loading the model parameters into image
RUN python model_cacher.py

# Start the container
CMD ["python3", "-u", "rp_handler.py"]

# Version Log [docker build --platform linux/amd64 --tag leejaehun314/tts-runpod-serverless:0.0.4 .]
# 0.0.1 - Initial version, with basic functionality.
# 0.0.2 - Update the model downloader to download open_jtask related files. Done for cold start inference time improvement.
# 0.0.3 - Refactor the code to make it more modular and readable.
# 0.0.4 - Mikke version.
# 0.0.4.1 - Add more video formats