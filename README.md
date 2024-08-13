---
title: Youtube Summary
emoji: 📺
colorFrom: gray
colorTo: green
sdk: streamlit
sdk_version: 1.37.0
app_file: app.py
pinned: false
license: mit
---

# YouTube AI Summarizer

이 웹앱은 Google의 생성형 AI를 사용하여 YouTube 동영상을 요약합니다. 동영상 링크를 붙여넣기만 하면 빠르게 요약을 얻을 수 있습니다!

### 기능

* YouTube 동영상을 요약합니다.
* Streamlit 프레임워크를 활용하여 인터랙티브한 웹 앱 경험을 제공합니다.

### 설치

1. **저장소를 복제합니다:**

   ```bash
   git clone https://github.com/anpigon/YouTube-AI-Summarizer.git
   cd YouTube-AI-Summarizer
   ```

2. **가상 환경을 만들고 활성화합니다:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **종속성을 설치합니다:**

   ```bash
   poetry install
   ```

### 구성

1. **Google Generative AI API 키를 얻습니다:**
   - Gemini API를 사용하려면 API 키가 필요합니다.
   - [API 키 가져오기](https://makersuite.google.com/app/apikey?hl=ko)에서 API 키를 생성합니다.

2. **API 키를 환경 변수로 설정합니다:**

   ```bash
   export GOOGLE_API_KEY="여러분의 GOOGLE API KEY"
   ```

### 사용법

1. **Streamlit 앱을 시작합니다:**

   ```bash
   poetry run streamlit run app.py
   ```

2. **브라우저에서 앱을 엽니다:**
   - 앱은 `http://localhost:8501/`에서 실행됩니다.

3. **YouTube 동영상 URL을 붙여넣고 "요약"을 클릭합니다.**

### References
- https://ai.google.dev/gemini-api/docs/vision?hl=ko&lang=python#prompting-video

### 기여

기여는 언제나 환영합니다! 제안이나 개선 사항이 있으면 이슈를 열거나 풀 리퀘스트를 제출해 주세요.

### 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 사용이 허가되었습니다.
