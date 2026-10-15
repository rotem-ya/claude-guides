#!/usr/bin/env python3
"""Install or update token-kit in a repository (new or existing). Idempotent: run it again to update.

    python3 install.py <repo-dir>

It copies tools/codemap.py (+ its TypeScript helper), adds the SessionStart hook (.claude/hooks/session-start.sh and its
entry in .claude/settings.json), gitignores docs/codemap/, writes the rules block into CLAUDE.md (between the token-kit
markers, replacing an older block), and builds the code map once. It never overwrites a hook the repository wrote itself:
it prints what to add instead.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
START, END = "<!-- token-kit:start", "<!-- token-kit:end -->"
HOOK_CMD = '"$CLAUDE_PROJECT_DIR"/.claude/hooks/session-start.sh'


def main(target: Path) -> None:
    if not (target / ".git").exists():
        sys.exit(f"not a git repository: {target}")
    notes = []

    tools = target / "tools"
    tools.mkdir(exist_ok=True)
    for f in ("codemap.py", "codemap_ts.cjs"):
        shutil.copy2(KIT / f, tools / f)
    (tools / "codemap.py").chmod(0o755)

    hooks = target / ".claude" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "session-start.sh"
    if hook.exists() and "token-kit" not in hook.read_text(encoding="utf-8"):
        if "codemap" not in hook.read_text(encoding="utf-8"):
            notes.append(f"{hook.relative_to(target)} is the repository's own: add `python3 tools/codemap.py` at its end")
    else:
        shutil.copy2(KIT / "session-start.sh", hook)
        hook.chmod(0o755)

    settings_p = target / ".claude" / "settings.json"
    settings = json.loads(settings_p.read_text(encoding="utf-8")) if settings_p.exists() else {}
    starts = settings.setdefault("hooks", {}).setdefault("SessionStart", [])
    if not any("session-start.sh" in h.get("command", "") for e in starts for h in e.get("hooks", [])):
        starts.append({"matcher": "startup", "hooks": [{"type": "command", "command": HOOK_CMD}]})
    settings_p.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    gi = target / ".gitignore"
    lines = gi.read_text(encoding="utf-8").splitlines() if gi.exists() else []
    if not any(l.strip().rstrip("/") == "docs/codemap" for l in lines):
        gi.write_text("\n".join(lines + ["docs/codemap/"]) + "\n", encoding="utf-8")

    rules = (KIT / "RULES.md").read_text(encoding="utf-8").strip()
    cm = target / "CLAUDE.md"
    text = cm.read_text(encoding="utf-8") if cm.exists() else f"# {target.name}: instructions for every Claude session\n"
    block = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    text = block.sub(lambda _: rules, text) if block.search(text) else text.rstrip() + "\n\n" + rules + "\n"
    cm.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")

    res = subprocess.run([sys.executable, str(tools / "codemap.py")], cwd=target, capture_output=True, text=True)
    print(res.stdout.strip() or res.stderr.strip())
    for n in notes:
        print("note:", n)
    print(f"token-kit installed in {target}: tools/codemap.py, .claude/hooks/session-start.sh, .claude/settings.json, .gitignore, CLAUDE.md")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve())
