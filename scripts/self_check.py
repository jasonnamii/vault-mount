#!/usr/bin/env python3
"""
vault-mount self-check
- 볼트 경로 존재·가독성 검증
- Agent-Ops/ 디렉토리 존재 확인
- 마운트 게이트 무결성 (SKILL.md 핵심 규칙 4개 확인)

Usage:
    python3 self_check.py             # 마운트 상태 검증
    python3 self_check.py --skill ../  # 스킬 무결성 검증
"""
import sys
import os
import json
from pathlib import Path

VAULT_PATH = "/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault"
AGENT_OPS = f"{VAULT_PATH}/Agent-Ops"


def check_mount():
    """볼트 마운트 상태 검증"""
    result = {"vault_exists": False, "agent_ops_exists": False, "readable": False, "status": "unknown"}

    if os.path.isdir(VAULT_PATH):
        result["vault_exists"] = True
        try:
            os.listdir(VAULT_PATH)
            result["readable"] = True
        except (PermissionError, OSError):
            result["readable"] = False

    if os.path.isdir(AGENT_OPS):
        result["agent_ops_exists"] = True

    if result["vault_exists"] and result["readable"]:
        result["status"] = "mounted" if result["agent_ops_exists"] else "mounted_but_no_agent_ops"
    else:
        result["status"] = "not_mounted"

    return result


def check_skill_integrity(skill_dir):
    """SKILL.md 핵심 규칙 4개 + frontmatter 무결성"""
    skill_md = Path(skill_dir) / "SKILL.md"
    if not skill_md.exists():
        return {"valid": False, "error": "SKILL.md not found"}

    content = skill_md.read_text(encoding="utf-8")
    checks = {
        "frontmatter": content.startswith("---"),
        "rule_1_path_fixed": VAULT_PATH in content,
        "rule_2_fail_continue": "STOP ✗" in content or "폴백 진행" in content,
        "rule_3_skip_if_mounted": "이미 마운트" in content or "already_mounted" in content,
        "rule_4_fallback_order": "코워크 빌트인" in content and "옵시디언 MCP" in content,
        "p1_keyword_경로": "경로" in content,  # 추가된 트리거
        "fallback_ref": "fallback-protocol" in content or "FS 작업 폴백" in content,
    }
    failed = [k for k, v in checks.items() if not v]
    return {"valid": len(failed) == 0, "checks": checks, "failed": failed}


if __name__ == "__main__":
    if "--skill" in sys.argv:
        skill_dir = sys.argv[sys.argv.index("--skill") + 1]
        result = check_skill_integrity(skill_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["valid"] else 1)
    else:
        result = check_mount()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["status"] in ("mounted", "mounted_but_no_agent_ops") else 1)
