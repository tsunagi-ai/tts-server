# raccoonpty-tts-server

Runpod Serverless 환경에서 구동되도록 설정된 TTS 인퍼런스 코드입니다. 

- 기존 코드의 인퍼런스 부분은 **rp_handler.py**에 있습니다. 
- 모델 설정에 관련된 내용을 **model_config.py**로 분리하였습니다. 
- 도커 이미지를 만드는 과정에서 모델 에셋을 caching하기 위해 **model_cacher.py**가 추가되었습니다. (모델 cache가 없으면 serverless 특성 상 매 인퍼런스마다 모델 파일을 다운로드하게 됨으로 비효율적입니다.)

# Quick Start

- 도커 이미지를 빌드하기 위해서는 아래 명령어를 사용하세요.

    ```
    $ docker build --platform linux/amd64 --tag <tag> .
    ```

- 인퍼런스를 테스트하려면 requirements.txt를 통해 dependency를 설치하고 rp_handler.py를 실행하세요. (*처음 실행할 때는 model_cacher.py를 먼저 실행해야 관련 모델 파일들이 다운로드 됩니다.)