#!/usr/bin/env python3
"""Build dist/token-kit.zip: the skill as one file to upload to a claude.ai account (Customize → Skills)."""
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = ["SKILL.md", "codemap.py", "codemap_ts.cjs", "install.py", "session-start.sh", "RULES.md", "AGENTS_BLOCK.md"]

if __name__ == "__main__":
    out = HERE / "dist" / "token-kit.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in FILES:
            z.write(HERE / f, f"token-kit/{f}")
    print(f"{out.relative_to(HERE.parent)}: {len(FILES)} files, {out.stat().st_size // 1024} KB")
