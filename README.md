# 이미지 플러그 판별 AI 서버

이 프로젝트는 이미지를 입력받아 플러그가 꽂혀 있는지 여부를 판별하는 AI 모델을 Flask 기반 REST API로 제공합니다.  
Azure Blob Storage에서 모델을 자동으로 다운로드하여 사용합니다.

## 주요 기능

- 이미지 업로드를 통한 플러그 판별 (`/predict` 엔드포인트)
- Docker 및 docker-compose 지원
- 예제 프론트엔드 코드 제공 (Node.js/axios)

---

## 설치 및 실행

### 1. Python 환경에서 직접 실행

```bash
# 패키지 설치
pip install -r requirements.txt

# 서버 실행
python app.py
```
### 2. docker-compose로 실행

```bash
docker-compose up --build
```

---

## API 사용법

### POST `/predict`

- **요청**: `multipart/form-data`로 이미지 파일(`file` 필드) 전송
- **응답**: JSON
  - `result`: "true" (꽂힘) 또는 "false" (안 꽂힘)
  - `score`: 플러그가 꽂혔을 확률 (0~1)

#### 예시 응답

```json
{
  "result": "false"
  "score": 0.1234,
}
```

---

## 예제 코드

### Node.js (axios)

```js
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const url = "http://localhost:8080/predict";
const imagePath = "./test-dataset/3.jpeg";

const form = new FormData();
form.append('file', fs.createReadStream(imagePath));

axios.post(url, form, { headers: { ...form.getHeaders() } })
  .then(response => console.log("Response:", response.data))
  .catch(console.error);
```

### Python

```python
import requests

url = "http://localhost:8080/predict"
image_path = "./test-dataset/3.jpeg"

with open(image_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print(response.json())
```

---

## 폴더 구조

- `app.py` : Flask API 서버
- `requirements.txt` : Python 의존성 목록
- `dockerfile`, `docker-compose.yaml` : 도커 환경 설정
- `front-example.js` : Node.js 프론트엔드 예제
- `test-dataset/` : 테스트용 이미지 샘플

---

## 참고

- 모델 파일(`full_model.pth`)은 Azure Blob Storage에서 자동 다운로드됩니다. (.env 추가 필요)
