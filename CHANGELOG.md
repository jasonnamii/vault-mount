# CHANGELOG — vault-mount

## v1.2 — 2026-05-07

### Added
- **PATH_TRIGGER (Rule 0)** — 절대 규칙 4개 → 5개로 확장. host 절대경로 패턴 hit 시 100% 강제발동, grep 우회·NOT 우회 ✗
- P1 트리거: `/Users/jason/`, `/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault`, `/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault/`, `/Users/jason/ObsidianVault`, `/Users/jason/ObsidianVault/`, `~/`, `host절대경로`, `경로패턴`, `path pattern`, `absolute path`
- ① 트리거 감지에 PATH_TRIGGER 최우선 블록 (정규식 `(/Users/jason/|~/)`)
- WRONG/CORRECT 1쌍 추가 (PATH_TRIGGER 케이스)
- 케이스 5: PATH_TRIGGER 절대경로 hit
- 케이스 6: PATH_TRIGGER `~/` 별칭 hit

### Changed
- description에 v1.2 PATH_TRIGGER 1줄 명시
- 절대 규칙 표 헤더 "4개" → "5개"
- frontmatter version v1.1 → v1.2

### Why
- 형 메시지에 host 절대경로(`/Users/jason/...`)가 박힌 경우 = 100% 파일작업 신호. 단어 매칭 트리거(P1)는 grep 우회 가능 → Rule 0으로 격상하여 미발동 차단.

## v1.0 — 2026-04-26

### Added
- `references/fallback-protocol.md` — FS 폴백 순서·파일 안전 룰·트러블슈팅 분리 (허브 슬림화)
- `scripts/self_check.py` — 마운트 상태 검증 + 스킬 무결성 검증 (CLI)
- `evals/cases.json` — 5 시나리오 회귀 케이스 (이미마운트·신규성공·거부·경로트리거·FS폴백)
- `LICENSE` — Proprietary
- frontmatter `version: v1.0` 필드
- frontmatter `vault_dependency: required` 선언
- P1 트리거: `경로` 추가 (사용자 요청)
- "## 절대 규칙 (INVARIANT)" 헤더 명시

### Changed
- 본문에서 FS 폴백·파일 안전 룰 섹션을 references로 이동 → 허브 ≤5KB 목표
- "핵심 규칙 (4개)" → "절대 규칙 (INVARIANT) — 4개" 표제 강화

### Fixed
- skill-doctor 진단(2026-04-26) P0 4건·P1 4건 처방 반영
  - ⑦-3 evals 부재 → cases.json 추가
  - ⑦-4 CHANGELOG·LICENSE 부재 → 본 파일·LICENSE 추가
  - ⑧-1 self-check 부재 → scripts/self_check.py 추가
  - ⑤-2 references/ 부재 → fallback-protocol.md 분리
  - ④-2 결정적 작업 LLM 강요 → self_check.py로 분리
  - ④-3 vault_dependency 미선언 → frontmatter 추가
  - ⑦-1 version 미선언 → frontmatter 추가
  - ⑦-2 INVARIANT 헤더 부재 → 절대규칙 헤더 강화
