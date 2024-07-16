# MediWhale Task

## 실행

```sh
docker-compose up --build -V
```

## 환경변수

루트폴더에 `.env` 생성

```
ENV
PORT
PROJECT_NAME
SQLALCHEMY_DATABASE_URL
SWAGGER_USERNAME
SWAGGER_PASSWORD
SECRET_KEY
ALGORITHM
```

## Docs

1. username과 pssword를 입력 후 문서 진입
2. `token_generate`로 token 생성 후 Authorize에 입력.
3. `ai_url` 입력
4. `uploadfile`에 `dcm` 파일을 업로드
