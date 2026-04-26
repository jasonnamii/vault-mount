---
name: vault-mount
description: 옵시디언 볼트(Dropbox) 자동 마운트·검증 게이트키퍼. 세션 시작·트리거 단어 감지 시 mcp__cowork__request_cowork_directory를 결정적으로 호출하고, 3단계 파일시스템 폴백(코워크 빌트인→옵시디언 MCP→Desktop Commander)을 강제. 마운트 실패시 1줄 보고 후 작업 진행(STOP ✗). UP §BOOTSTRAP과 이중 안전장치.
P1: 볼트마운트, vault mount, vault-mount, 볼트, 마운트, mount, 시작, resume, 이어서, 볼트연결, 볼트접속, 볼트확인, 옵시디언마운트, obsidian mount, 드롭박스마운트.
P2: 마운트해줘, 연결해줘, 볼트 켜줘, 시작하자, 이어서 하자, mount it, connect vault.
P3: vault mount, dropbox mount, obsidian vault, file system bootstrap, mount gateway.
P4: 세션 시작 직후, 작업 재개시, 파일 작업 직전, 글로벌 CLAUDE.md FS_ACCESS 폴백 적용시.
P5: 마운트 결과 1줄 보고로.
NOT: UP수정(→up-manager), 스킬생성(→skill-builder), 세션브리핑(→session-briefing), 산출물생성(→paper-engine).
---

# vault-mount

옵시디언 볼트 마운트를 **결정적으로** 보장하는 인프라 게이트키퍼. UP §BOOTSTRAP과 함께 이중 안전장치.

**WHY:** 글로벌 CLAUDE.md의 MOUNT 선언(`MOUNT ::= request_cowork_directory 자동 마운트`)은 plugin-cache 경로에 있어 매 세션 재주입이 보장되지 않음. UP §BOOTSTRAP이 1차, 이 스킬이 2차 강제.

---

## 핵심 규칙 (4개)

| # | 규칙 | 위반 시 |
|---|------|--------|
| 1 | **볼트 경로 고정** — `/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault` (하드코딩 ✗ 원칙의 유일 예외, 형 전용) | 다른 경로로 마운트 = FAIL |
| 2 | **마운트 실패 = 보고+진행** — STOP ✗. `outputs/` 폴백으로 작업 계속, 1줄 경고만 | 작업 흐름 차단 = 형 생산성 손실 |
| 3 | **이미 마운트됨 = 스킵** — `ls VAULT/Agent-Ops` 1회 검증. 성공 = 재마운트 ✗ | 중복 마운트 = 형에게 권한 팝업 재노출 |
| 4 | **3단계 폴백 순서 강제** — ①코워크 빌트인 → ②옵시디언 MCP → ③Desktop Commander. 앞 단계 실패시만 다음 | 임의 폴백 = 디버깅 혼선 |

---

## 흐름 (선형 1턴)

```
① 트리거 감지 → ② 마운트 상태 검증 → ③ 마운트 호출 (필요시) → ④ 1줄 보고
```

### ① 트리거 감지

**자동 발동 조건 (하나라도 hit):**
- 세션 첫 사용자 메시지 (UP §BOOTSTRAP과 중복 방어)
- P1 트리거 단어 hit (볼트·마운트·시작·resume·이어서)
- 파일 작업 직전 + 마운트 미확인 상태
- 글로벌 CLAUDE.md FS_ACCESS 룰 적용 필요시

### ② 마운트 상태 검증 (Bash 1회)

```bash
ls /Users/jason/Library/CloudStorage/Dropbox/ObsidianVault/Agent-Ops/ 2>&1 | head -3
```

| 결과 | 판정 | 다음 |
|------|------|------|
| 디렉토리 정상 출력 | already_mounted | ④ 보고 1줄 ("✅ 볼트 이미 마운트됨") |
| `No such file` 또는 권한 거부 | 미마운트 | ③ 마운트 호출 |

### ③ 마운트 호출

```
mcp__cowork__request_cowork_directory(path="/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault")
```

**결과 분기:**
- ✅ 성공 → ④ 보고 ("✅ 볼트 마운트 완료")
- ❌ 사용자 거부·실패 → ④ 보고 ("⚠️ 볼트 마운트 실패 — outputs 폴백 진행") + 작업 계속

### ④ 보고 (1줄)

| 케이스 | 보고 문구 |
|--------|----------|
| 이미 마운트됨 | `✅ 볼트 이미 마운트됨` |
| 신규 마운트 성공 | `✅ 볼트 마운트 완료` |
| 마운트 실패 | `⚠️ 볼트 마운트 실패 — outputs 폴백 진행` |

스킵 조건: 일반 대화·실행 보고 (FS 작업 무관시 보고 생략).

---

## FS 작업 폴백 순서 (FS_ACCESS)

파일 읽기·쓰기·이동·목록·검색 시 다음 순서로 시도:

| 우선순위 | 도구군 | 예시 |
|----------|--------|------|
| ① | 코워크 빌트인 | Read · Write · Edit · Glob · Grep · Bash |
| ② | 옵시디언 MCP | mcp__obsidian__read_note · write_note · search_notes |
| ③ | Desktop Commander | mcp__Desktop_Commander__read_file · write_file |

**RULE:** 앞 단계 실패·불가 시에만 다음 단계로. 3단계 전부 실패 = STOP + 형에게 보고.

---

## 파일 안전 룰 (글로벌 CLAUDE.md 흡수)

| # | 룰 |
|---|---|
| 1 | `Write` 덮어쓰기 ✗ → `Edit` 사용 |
| 2 | 삭제 → `_archive/` 이동 (영구삭제 ✗) |
| 3 | 볼트 경로 = MOUNT resolve 결과 사용 (하드코딩 ✗, 단 마운트 호출 자체는 예외) |

---

## Gotchas

| 함정 | 대응 |
|------|------|
| 매 턴 마운트 호출 | ② 검증 단계로 already_mounted 판정 후 스킵. 형에게 권한 팝업 반복 노출 ✗ |
| 마운트 실패 시 STOP | 룰 #2 위반. 보고만 하고 작업 진행. outputs 폴백으로 산출 |
| 볼트 경로 다른 폴더 | 룰 #1 위반. 정확히 `/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault` |
| UP §BOOTSTRAP과 중복 호출 | 의도된 이중 안전장치. ② 검증으로 실제 호출은 1회만 발생 |
| 옵시디언 MCP 우선 시도 | 폴백 순서 위반. 코워크 빌트인 먼저 |
| 볼트 검증을 mcp__obsidian__로 | 코워크 빌트인 ls가 가장 빠름. MCP는 빌트인 실패시만 |
| 글로벌 CLAUDE.md만 믿기 | plugin-cache 경로 = 매 턴 주입 보장 ✗. 이 스킬 + UP이 진짜 강제 메커니즘 |

---

## 예시

**케이스 1: 세션 첫 메시지 "이어서 하자"**
```
hit: "이어서" (P1)
→ ② Bash: ls VAULT/Agent-Ops/ → 정상
→ ④ 보고: ✅ 볼트 이미 마운트됨
```

**케이스 2: 파일 작업 직전 미마운트**
```
사용자: "UP 좀 수정해줘"
→ ② Bash: ls VAULT/Agent-Ops/ → No such file
→ ③ request_cowork_directory(path="...ObsidianVault") → 성공
→ ④ 보고: ✅ 볼트 마운트 완료
→ up-manager 발동
```

**케이스 3: 마운트 실패**
```
hit: "볼트"
→ ② 미마운트 → ③ 호출 → 사용자 거부
→ ④ 보고: ⚠️ 볼트 마운트 실패 — outputs 폴백 진행
→ 작업 계속 (STOP ✗)
```
