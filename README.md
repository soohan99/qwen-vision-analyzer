# Qwen3.5 Vision 영상 분석기

On-Device AI(WebGPU)를 활용하여 YouTube 영상의 특정 화면을 분석하는 웹 애플리케이션입니다.
Qwen2.5-VL-0.5B 모델을 브라우저에서 직접 실행하여 화면을 한국어로 설명합니다.

## 기술 스택

| 구성 요소 | 기술 |
|-----------|------|
| AI 모델 | `onnx-community/Qwen2.5-VL-0.5B-Instruct-ONNX` |
| 추론 환경 | WebGPU (브라우저 내 On-Device) |
| AI 라이브러리 | Transformers.js v3.3.3 |
| 백엔드 | Python Flask + yt-dlp |
| 프레임 캡처 | Canvas API → RawImage |

## 실행 방법

### 사전 요구사항

- Python 3.8 이상
- **Chrome 113+** 또는 Edge (WebGPU 필수)
- 인터넷 연결 (모델 최초 다운로드 시 약 500MB)

### 1. 저장소 클론

```bash
git clone <레파지토리 URL>
cd work01
```

### 2. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 서버 실행

```bash
python3 app.py
```

터미널에 아래 메시지가 나타나면 성공입니다:
```
앱이 실행되었습니다! 브라우저에서 http://localhost:8080 을 열어주세요.
```

### 4. 브라우저에서 접속

Chrome 또는 Edge 브라우저로 `http://localhost:8080` 접속

## 사용 방법

1. **모델 로드** - "모델 로드" 버튼 클릭 (최초 실행 시 약 500MB 다운로드, 이후 브라우저 캐시 사용)
2. **영상 다운로드** - YouTube URL 입력 후 "다운로드" 버튼 클릭
3. **화면 분석** - 영상 재생 후 원하는 장면에서 일시정지 → "화면 분석" 버튼 클릭
4. **결과 확인** - 우측 패널에 AI가 분석한 한국어 설명이 스트리밍으로 출력됨

## 프로젝트 구조

```
work01/
├── app.py              # Flask 백엔드 (YouTube 다운로드, 비디오 서빙)
├── requirements.txt    # Python 의존성
├── README.md           # 실행 가이드
├── templates/
│   └── index.html      # 프론트엔드 (비디오 플레이어 + WebGPU AI 추론)
├── static/
│   └── style.css       # 스타일시트
└── downloads/          # 다운로드된 영상 임시 저장 (자동 생성)
```

## 주의사항

- WebGPU는 **Chrome 113+ 또는 Edge**에서만 지원됩니다 (Safari, Firefox 미지원)
- 모델 최초 로드 시 약 500MB를 다운로드하며 수 분이 소요됩니다 (이후 브라우저 캐시 활용)
- YouTube 저작권 정책에 따라 일부 영상은 다운로드가 제한될 수 있습니다
- 영상은 서버의 `downloads/` 폴더에 임시 저장되며, 새로운 다운로드 시 기존 파일이 삭제됩니다
