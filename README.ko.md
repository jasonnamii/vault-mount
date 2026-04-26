# vault-mount

옵시디언 볼트(Dropbox) 자동 마운트·검증 게이트키퍼.

## 무엇

세션 시작·트리거 단어 감지 시 `mcp__cowork__request_cowork_directory`를 결정적으로 호출. 3단계 파일시스템 폴백 강제(코워크 빌트인 → 옵시디언 MCP → Desktop Commander).

## 왜

글로벌 `CLAUDE.md`의 MOUNT 선언은 plugin-cache 경로에 있어 매 세션 재주입 보장 ✗. 이 스킬은 `UP §BOOTSTRAP`과 함께 이중 안전장치.

## 트리거

- P1: 볼트, 마운트, 시작, resume, 이어서
- P2: 마운트해줘, 연결해줘, 시작하자
- 자동: 세션 시작, 파일 작업 직전

## 실패 모드

마운트 실패 → 1줄 보고(`⚠️ 볼트 마운트 실패 — outputs 폴백 진행`) + 작업 계속. STOP ✗.

## 관련

- `README.md` — 영문 버전
- `UP §BOOTSTRAP` — 1차 강제 레이어 (매 턴 주입)
