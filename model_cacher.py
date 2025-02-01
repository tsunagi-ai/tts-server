# Model related
from pathlib import Path
import torch
from style_bert_vits2.nlp import bert_models
from style_bert_vits2.constants import Languages
from style_bert_vits2.tts_model import TTSModel, TTSModelHolder
from huggingface_hub import hf_hub_download

import model_config

# Downloading BERT models
bert_models.load_model(Languages.JP, model_config.bert_model)
bert_models.load_tokenizer(Languages.JP, model_config.bert_tokenizer)

model_file = model_config.model_file
config_file = model_config.config_file
style_file = model_config.style_file

# Downloading model files
for file in [model_file, config_file, style_file]:
    hf_hub_download("nonmetal/jvnv-test", file, local_dir="model_assets")

model_dir = Path("model_assets")
device = "cuda" if torch.cuda.is_available() else "cpu"

# Downaloading "https://github.com/r9y9/open_jtalk/releases/download/v1.11.1/open_jtalk_dic_utf_8-1.11.tar.gz"
# via running the model once, this will save that file into the environment
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

model = loaded_models[0]
sr, audio = model.infer(
    text="おはよう!",
    language="JP",
    speaker_id=0,
)
