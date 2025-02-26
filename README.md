# raccoonpty-tts-server

This is a TTS inference code configured to run in a **Runpod Serverless** environment.

- The inference logic from the original code is located in **rp_handler.py**.
- Model configuration settings have been separated into **model_config.py**.
- **model_cacher.py** has been added to cache model assets during the Docker image build process.  
  (Without model caching, the serverless environment would download model files for each inference, leading to inefficiency.)

---

# Quick Start

- To build the Docker image, run the following command:

    ```
    $ docker build --platform linux/amd64 --tag <tag> .
    ```

- To test inference, install dependencies from `requirements.txt` and run `rp_handler.py`.  
  (*On the first execution, run `model_cacher.py` first to download the necessary model files.)
