---
name: vault-mount
description: "옵시디언 볼트(Dropbox) 자동 마운트 게이트키퍼. **모든 파일 작업·VAULT 접근·Read/Write/Edit/Bash 직전 자동선행**. 세션 첫 메시지·재개·이어서·resume·볼트·마운트·옵시디언·드롭박스·VAULT·파일·노트·메모·저장·읽기·쓰기·검색 등 트리거 hit 시 mcp__cowork__request_cowork_directory를 결정적 호출. 3단계 폴백(코워크 빌트인→옵시디언 MCP→Desktop Commander). 마운트 실패시 1줄 보고 후 outputs 폴백으로 작업 진행(STOP ✗). UP §BOOTSTRAP과 이중 안전장치. 권한 팝업 중복 ✗ — already_mounted 검증 스킵 내장."
version: v1.1
vault_dependency: required
license: "Proprietary. LICENSE has complete terms."
P1: 볼트마운트, 볼트, vault, vault mount, vault-mount, 마운트, mount, 자동마운트, 시작, 재개, resume, 이어서, 이어하자, 볼트연결, 볼트접속, 볼트확인, 볼트체크, 볼트경로, vault path, 옵시디언, 옵시디언볼트, obsidian, obsidian vault, 옵시디언마운트, obsidian mount, 드롭박스, dropbox, 드롭박스마운트, 경로, 경로확인, FS, FS_ACCESS, 파일시스템, file system, 파일접근, 노트접근, 볼트접근, vault access, BOOTSTRAP, 부트스트랩, 게이트키퍼, gatekeeper, 자동선행, 강제선행, 마운트선행, 선행마운트.
P2: 마운트해줘, 연결해줘, 볼트 켜줘, 볼트 마운트해줘, 볼트 열어줘, 볼트 띄워줘, 볼트 붙여줘, 시작하자, 이어서 하자, 이어가자, 재개하자, 다시 시작, mount it, connect vault, mount vault, 경로 확인, 볼트 어디야, 볼트 경로, 볼트 잘 되나, 볼트 살아있나, 파일 접근 가능해, 노트 접근 가능해, VAULT 접근, 옵시디언 켜줘, 드롭박스 연결해줘.
P3: vault mount, dropbox mount, obsidian vault mount, file system bootstrap, mount gateway, vault path resolve, request_cowork_directory, fs access bootstrap, mount precondition, fs precondition.
P4: 세션 시작 직후 (첫 사용자 메시지), 작업 재개·이어서 시, **모든 파일 작업 직전 (Read/Write/Edit/Bash·옵시디언 노트·VAULT 접근)**, 글로벌 CLAUDE.md FS_ACCESS 폴백 적용시, 볼트 경로 조회·검증시, UP §BOOTSTRAP 미발동 의심시, 다른 스킬(up-manager·skill-builder·session-briefing·project-updater 등)이 VAULT 접근 직전.
P5: 마운트 결과 1줄 보고로 (✅이미마운트 / ✅마운트완료 / ⚠️실패-폴백).
NOT: UP수정(→up-manager), 스킬생성·수정(→skill-builder), 세션브리핑(→session-briefing), 프로젝트초기화(→project-updater), 산출물생성(→shaper-skill), 일반리서치(→research-skill).
---

# vault-mount

옵시디언 볼트 마운트를 **결정적으로** 보장하는 인프라 게이트키퍼. UP §BOOTSTRAP과 함께 이중 안전장치.

**WHY:** 글로벌 CLAUDE.md의 MOUNT 선언(`MOUNT ::= request_cowork_directory 자동 마운트`)은 plugin-cache 경로에 있어 매 세션 재주입이 보장되지 않음. UP §BOOTSTRAP이 1차, 이 스킬이 2차 강제.

---

## 절대 규칙 (INVARIANT) — 4개

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
- P1 트리거 단어 hit (볼트·마운트·시작·resume·이어서·경로)
- 파일 작업 직전 + 마운트 미확인 상태
- 글로벌 CLAUDE.md FS_ACCESS 룰 적용 필요시
- 볼트 경로 조회·확인 요청 ("경로 알려줘"·"볼트 어디야")

### ② 마운트 상태 검증 (Bash 1회)

```bash
ls /Users/jason/Library/CloudStorage/Dropbox/ObsidianVault/Agent-Ops/ 2>&1 | head -3
```

| 결과 | 판정 | 다음 |
|------|------|------|
| 디렉토리 정상 출력 | already_mounted | ④ 보고 1줄 ("✅ 볼트 이미 마운트됨") |
| `No such file` 또는 권한 거부 | 미마운트 | ③ 마운트 호출 |

**또는 `scripts/self_check.py` 실행으로 자동화:**
```bash
python3 scripts/self_check.py
# 출력: {"status": "mounted" | "not_mounted", ...}
```

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

## FS 폴백 + 파일 안전 룰

상세 프로토콜: `→ references/fallback-protocol.md 참조`

핵심 요약 1줄: **코워크 빌트인 → 옵시디언 MCP → Desktop Commander 순서. 3단계 모두 실패 = STOP. Write 덮어쓰기 ✗ → Edit. 삭제 → _archive/.**

---

## 자기 진단 (self-check)

```bash
# 마운트 상태 검증
python3 scripts/self_check.py

# 스킬 무결성 검증 (절대규칙 4개 + frontmatter)
python3 scripts/self_check.py --skill ./
```

회귀 케이스: `evals/cases.json` (5 시나리오)

---

## Gotchas

| 함정 | 대응 |
|------|------|
| 매 턴 마운트 호출 | ② 검증 단계로 already_mounted 판정 후 스킵. 형에게 권한 팝업 반복 노출 ✗ |
| 마운트 실패 시 STOP | 절대규칙 2 위반. 보고만 하고 작업 진행. outputs 폴백으로 산출 |
| 볼트 경로 다른 폴더 | 절대규칙 1 위반. 정확히 `/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault` |
| UP §BOOTSTRAP과 중복 호출 | 의도된 이중 안전장치. ② 검증으로 실제 호출은 1회만 발생 |
| 옵시디언 MCP 우선 시도 | 폴백 순서 위반. 코워크 빌트인 먼저 (`→ references/fallback-protocol.md`) |
| 볼트 검증을 mcp__obsidian__로 | 코워크 빌트인 ls가 가장 빠름. MCP는 빌트인 실패시만 |
| 글로벌 CLAUDE.md만 믿기 | plugin-cache 경로 = 매 턴 주입 보장 ✗. 이 스킬 + UP이 진짜 강제 메커니즘 |
| host 경로와 VM 경로 혼동 | host=`/Users/jason/...`, VM=`/sessions/{id}/mnt/...`. Read/Write/Edit는 host, Bash는 VM |

### ❌ WRONG vs ✅ CORRECT

```
❌ WRONG: 매 턴 request_cowork_directory 호출 (검증 단계 스킵 → 권한 팝업 반복)
✅ CORRECT: ls VAULT/Agent-Ops/ 검증 → 정상이면 already_mounted → 호출 스킵
```

```
❌ WRONG: 마운트 실패 → STOP + 사용자 보고 후 작업 중단
✅ CORRECT: 마운트 실패 → 1줄 경고 + outputs 폴백으로 작업 계속 (절대규칙 2)
```

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

**케이스 4: 경로 트리거 (v1.0 신규)**
```
사용자: "볼트 경로 확인해줘"
hit: "경로" (P1)
→ ② 마운트 검증 → 정상
→ ④ 보고: ✅ 볼트 이미 마운트됨 — /Users/jason/Library/CloudStorage/Dropbox/ObsidianVault
```

---

## 변경 이력

`→ CHANGELOG.md 참조`
