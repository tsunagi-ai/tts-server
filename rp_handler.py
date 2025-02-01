# Model related
from pathlib import Path
import torch
from style_bert_vits2.nlp import bert_models
from style_bert_vits2.constants import Languages
from style_bert_vits2.tts_model import TTSModel, TTSModelHolder

import model_config

# Encoding related
from io import BytesIO
from scipy.io import wavfile
import base64

# Runpod related
import runpod
import datetime
import inspect

# Simple logging function similar to runpod's logger
def log(message, level="INFO"):
    """
    Prints a log message to the console in the format:
    MM-DD HH:MM:SS | LEVEL | filename.py:line_no | message
    """
    now_str = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
    # `inspect.stack()[1]` is the caller's stack frame
    caller = inspect.stack()[1]
    filename = caller.filename
    lineno = caller.lineno

    print(f"{now_str} | HANDLER-{level} | {filename}:{lineno} | {message}")

# Load BERT models
bert_models.load_model(Languages.JP, model_config.bert_model)
bert_models.load_tokenizer(Languages.JP, model_config.bert_tokenizer)

# Define path
model_file = model_config.model_file
config_file = model_config.config_file
style_file = model_config.style_file    

# TTS model loading
log("Loading TTS models...")
model_dir = Path("model_assets")
device = "cuda" if torch.cuda.is_available() else "cpu"

log(f"Inference device is set to: {device}")
model_holder = TTSModelHolder(model_dir, device)
loaded_models = []
for model_name, model_paths in model_holder.model_files_dict.items():
    model = TTSModel(
        model_path=model_dir / model_file,
        config_path=model_dir / config_file,
        style_vec_path=model_dir / style_file,
        device=model_holder.device,
    )
    loaded_models.append(model)
log(f"Model loading complete: {len(loaded_models)}")

# Runpod handler
def handler(event):
    data = event["input"]
    text = data.get("text")
    model_id = data.get("model_id", 0)
    speaker_id = data.get("speaker_id", 0)
    language = data.get("language", "JP")

    log(f"Received request with text: {text}, model_id: {model_id}, speaker_id: {speaker_id}, language: {language}")

    if model_id >= len(loaded_models):
        error_message = "Invalid model_id"
        log(f"Error: {error_message}")
        return {'error': error_message}

    model = loaded_models[model_id]

    try:
        sr, audio = model.infer(
            text=text,
            language=language,
            speaker_id=speaker_id,
        )
        log(f"Audio synthesized successfully with sample rate: {sr} and audio length: {len(audio)}")

    except Exception as e:
        error_message = f"Error during synthesis: {e}"
        log(f"Error: {error_message}")
        return {"error": error_message}

    # Convert audio to wav format
    wav_io = BytesIO()
    wavfile.write(wav_io, sr, audio)
    wav_io.seek(0)

    # Read raw bytes from buffer
    wav_bytes = wav_io.read()
    # Encode to Base64
    wav_base64 = base64.b64encode(wav_bytes).decode('utf-8')

    return {"wav_base64": wav_base64}

if __name__ == "__main__":
    runpod.serverless.start({'handler': handler})