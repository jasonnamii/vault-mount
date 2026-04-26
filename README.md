# vault-mount

Obsidian vault auto-mount + verification gatekeeper for Cowork sessions.

## What it does

Deterministically calls `mcp__cowork__request_cowork_directory` at session start or when trigger words are detected (볼트·마운트·시작·resume·이어서). Enforces 3-tier file system fallback: Cowork builtin → Obsidian MCP → Desktop Commander.

## Why

Global `CLAUDE.md` MOUNT declarations are stored in plugin-cache paths and not guaranteed to be re-injected per session. This skill, paired with `UP §BOOTSTRAP`, provides dual safety enforcement.

## Triggers

- P1: 볼트, 마운트, 시작, resume, 이어서, vault, mount
- P2: 마운트해줘, 연결해줘, 시작하자, mount it
- Auto: session-start, file-op preludes

## Failure mode

Mount failure → 1-line report (`⚠️ 볼트 마운트 실패 — outputs 폴백 진행`) + continue work. Never STOP.

## See also

- `README.ko.md` — Korean version
- `UP §BOOTSTRAP` — primary enforcement layer (per-turn injection)
