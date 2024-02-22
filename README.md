# Slack Auto Reaction

**아무도 상처받지 않는 세상을 위해 Slack 메시지에 자동으로 자연스러운 리액션을 추가하자!**

이 프로그램은 모든 사용자가 서로를 더 쉽게 이해하고 따뜻한 반응을 나눌 수 있는 환경을 조성하기 위해 개발되었습니다. 바쁜 일상 속에서 때때로 메시지에 즉각적으로 반응할 수 없는 상황이 생기는데, 이때 자동 리액션 프로그램이 소통의 간극을 메웁니다.

이 프로그램을 통해 사용자는 서로의 메시지에 자연스러운 반응을 할 수 있게 되어, 모두가 연결되어 있고 소중한 존재라는 느낌을 공유할 수 있습니다. 바쁘거나 반응을 표현하는 것을 잊었을 때에도, 이 프로그램이 긍정적이고 배려 깊은 방식으로 대신 표현해 줍니다.

## 기능

1. 많은 사람들이 반응하는 메시지에 같은 반응을 추가합니다.
2. 채널의 전부를 호출하는 메시지에 반응을 추가합니다.
3. 나를 호출하는 메시지에 반응을 추가합니다.
4. 나와 관련된 팀을 호출하는 메시지에 반응을 추가합니다.
<details>
<summary>(선택) 위의 행동을 수행하고 DM을 통해 보고합니다.</summary>
 
![image](https://github.com/DaeHyeoNi/slack-autoreaction/assets/1341628/8d7fd1c1-c3d8-4ace-9206-8e8fcdbee327)

</details>

## 설치 방법

### 환경 설정
1. `.env.example` 파일을 복사하여 `.env` 파일을 만듭니다.
2. `.env` 파일 내에 필요한 환경변수를 설정합니다.

### Slack API Token 발급
 - Slack API Token은 [Slack API](https://api.slack.com/)에서 발급받을 수 있습니다. [이러한 가이드](https://jimmy-ai.tistory.com/422)를 참고하여 발급받으세요.

### 프로그램 설치 및 실행
```bash
cp .env.example .env

pipenv install
pipenv run main.py
```

### 필요한 Slack 권한

- `reactions:write` : 메시지에 리액션을 추가하기 위해 필요합니다.
- `groups:history` : 채널 내 메시지 히스토리를 읽기 위해 필요합니다.
- `chat:write` :  (선택 사항) 1:1 DM을 통한 결과 전송 기능을 사용할 경우 필요합니다. `REPORT_RESULT_TO_DM` 환경변수를 `False`로 설정하면 이 권한은 필요하지 않습니다.

[권한설정은 이 사진을 참고하세요.](https://github.com/DaeHyeoNi/slack-autoreaction/assets/1341628/acb5db86-edcc-4fcf-ae60-be283ea923d6)
<br /><br /><br />


![](https://github.com/DaeHyeoNi/slack-autoreaction/assets/1341628/1409afe8-78bd-4a22-91f6-0b14d79aa633)
