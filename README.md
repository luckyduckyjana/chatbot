# 💬 Chatbot template

A simple Streamlit app that shows how to build a chatbot using OpenAI models.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
### App 사용법 (모델 테스트)

- 사이드바의 `Model Settings`를 펼쳐서 모델을 선택합니다.
- `System prompt`에 시스템 프롬프트를 입력하면 대화의 초기 메시지로 적용됩니다.
- `Temperature` 슬라이더로 응답의 창의성(무작위성)을 조절합니다.
- `Max Tokens`로 모델이 생성할 최대 토큰 수를 설정합니다.
- `OpenAI API Key`를 입력하면 실제 OpenAI 모델에 요청합니다. 비워두면 로컬 모의(Mock) 응답으로 동작하여 바로 테스트할 수 있습니다.

### 환경 변수

- 실제 OpenAI를 사용하려면 `OPENAI_API_KEY` 환경 변수를 설정하거나 앱 사이드바에 키를 입력하세요.
