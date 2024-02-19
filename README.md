# Slack Auto Reaction

Slack에 자동으로 자연스러운 리액션을 하자

이 프로그램은 모두가 상처받지 않는 세상을 위해 만들어졌습니다.
누군가가 내 메시지에 이모지를 달지 않는다고 슬퍼하지 말아요. 😢 그사람은 그냥 귀찮아서 안누른걸꺼야..

그런 귀찮은 당신을 위해 이 프로그램을 만들었습니다. 😊

이 프로그램은 아래와 같은 동작을 수행합니다.

1. 많은 사람들이 반응하는 메시지에 같은 반응을 추가합니다.
2. 채널의 전부를 호출하는 메시지에 반응을 추가합니다.
3. 나를 호출하는 메시지에 반응을 추가합니다.
4. 나와 관련된 팀을 호출하는 메시지에 반응을 추가합니다.

## How to Install

.env.example 파일을 복사하여 .env 파일을 만들고 환경변수를 설정합니다.

환경 변수 내 Slack API Token은 [Slack API](https://api.slack.com/)에서 발급받을 수 있습니다. [이러한 가이드](https://jimmy-ai.tistory.com/422)를 참고하세요.

```bash
cp .env.example .env

pipenv install
pipenv run main.py
```

## Requires Scope

- `reactions:write`
- `groups:history`
- `chat:write`  (Optional) 1:1 DM을 통한 결과 전송 `REPORT_RESULT_TO_DM` 환경변수를 `False`로 설정하면 필요하지 않습니다.
