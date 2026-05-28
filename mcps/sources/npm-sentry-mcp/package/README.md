# Sentry MCP Server

Sentry MCP(Model Context Protocol) 서버는 AI 모델이 Sentry 이슈를 조회하고 분석할 수 있게 해주는 도구입니다.

## 설치

```bash
npm install
```

## 환경 변수 설정

다음 환경 변수를 설정해야 합니다:

- `SENTRY_AUTH_TOKEN`: Sentry API 토큰
- `SENTRY_ORGANIZATION`: Sentry 조직 이름
- `TRANSPORT`: (선택) 전송 방식 설정 (`stdio` 또는 기본값인 HTTP/SSE)

## 실행 방법

개발 모드로 실행:

```bash
npm run dev
```

또는 환경 변수와 함께 실행:

```bash
SENTRY_AUTH_TOKEN=your_token SENTRY_ORGANIZATION=your_org npm run dev
```

빌드 후 실행:

```bash
npm run build
SENTRY_AUTH_TOKEN=your_token SENTRY_ORGANIZATION=your_org node dist/index.js
```

## API 엔드포인트

HTTP/SSE 모드에서는 다음 엔드포인트를 사용할 수 있습니다:

- GET `/sse`: SSE 연결 설정
- POST `/messages`: 메시지 전송

서버는 기본적으로 3000번 포트에서 실행됩니다.
