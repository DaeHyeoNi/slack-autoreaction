# Slack Auto Reaction

Slack에 자동으로 자연스러운 리액션을 하자

## How to Install

.env.example 파일을 복사하여 .env 파일을 만들고 환경변수를 설정한다.

Slack API Token은 [Slack API](https://api.slack.com/)에서 발급받을 수 있다. [이러한 가이드](https://jimmy-ai.tistory.com/422)를 참고하여 발급가능하다.

```bash
pipenv install
pipenv run main.py
```

## 필요한 Scope

- `reactions:write`
- `groups:history`
