# Fallback Protocol — FS 폴백 순서 + 파일 안전 룰

vault-mount의 본문 허브에서 분리된 상세 프로토콜. 본문은 표·결정 로직만, 본 문서는 룰의 원본·이유·예외 처리.

---

## FS 작업 폴백 순서 (FS_ACCESS)

파일 읽기·쓰기·이동·목록·검색 시 다음 순서로 시도. 앞 단계 실패·불가 시에만 다음.

| 우선순위 | 도구군 | 예시 도구 | 사용 조건 |
|----------|--------|----------|----------|
| ① | 코워크 빌트인 | Read · Write · Edit · Glob · Grep · Bash | 기본. 가장 빠르고 안정적 |
| ② | 옵시디언 MCP | mcp__obsidian__read_note · write_note · search_notes | ① 실패 또는 옵시디언 frontmatter·wikilink 조작 필요 시 |
| ③ | Desktop Commander | mcp__Desktop_Commander__read_file · write_file | ②까지 실패 또는 .DS_Store·시스템 파일 접근 필요 시 |

**3단계 전부 실패 = STOP + 사용자 보고.** 임의 폴백·도구 혼용 금지.

### WHY 우선순위
- 코워크 빌트인은 host filesystem 직접 접근 → 지연 최소
- 옵시디언 MCP는 vault 메타데이터(frontmatter·wikilink) 인식
- Desktop Commander는 모든 경로 접근 가능하나 가장 느림

---

## 파일 안전 룰 (글로벌 CLAUDE.md 흡수)

| # | 룰 | 이유 |
|---|---|---|
| 1 | `Write` 덮어쓰기 ✗ → `Edit` 사용 | Write는 전체 파일 재작성 → 의도치 않은 손실 위험 |
| 2 | 삭제 → `_archive/` 이동 (영구삭제 ✗) | 복구 가능성 보존 |
| 3 | 볼트 경로 = MOUNT resolve 결과 사용 | 하드코딩은 절대규칙 위반 (단, 마운트 호출 자체는 예외 — 형 전용 고정 경로) |

### 파일 작업 결정 트리

```
파일 작업 요청
├─ 새 파일 생성 → Write (충돌 가능성 0)
├─ 기존 파일 수정 → Edit (Write 금지)
├─ 파일 이동·이름변경 → Bash mv
└─ 파일 삭제 → _archive/로 이동 (rm 금지)
```

---

## 마운트 검증 상세

### 정상 출력 케이스
```bash
$ ls /Users/jason/Library/CloudStorage/Dropbox/ObsidianVault/Agent-Ops/ 2>&1 | head -3
_skill-doctor
_session_briefing
_skills research
```
→ `already_mounted` 판정. 재마운트 시도 ✗.

### 실패 케이스
```bash
$ ls /Users/jason/Library/CloudStorage/Dropbox/ObsidianVault/Agent-Ops/ 2>&1
ls: cannot access '...': No such file or directory
```
→ 미마운트 판정. `mcp__cowork__request_cowork_directory` 호출.

### Agent-Ops 디렉토리 부재 (특수)
볼트는 마운트됐으나 Agent-Ops 폴더 자체가 없으면 → 신규 사용자. 마운트는 성공이므로 `Agent-Ops/` 자동 생성 후 진행.

---

## 트러블슈팅

| 증상 | 원인 추정 | 처방 |
|------|----------|------|
| 권한 거부 (Permission denied) | Dropbox 동기화 중 lock | 5초 대기 후 재시도. 1회만 |
| 디렉토리 일부만 보임 | 클라우드 lazy load | `find /path -maxdepth 2` 강제 워크 |
| 마운트 호출 후 응답 없음 | 사용자가 권한 팝업 무시 | 30초 timeout → 보고 후 outputs 폴백 |
| 마운트는 됐으나 Read 실패 | host vs VM 경로 혼동 | host 경로(`/Users/jason/...`)와 VM 경로(`/sessions/{id}/mnt/...`) 분리 사용 |

