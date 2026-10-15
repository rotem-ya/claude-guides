"""Tests of token-kit's codemap.py and install.py: python3 -m pytest -q token-kit (from the claude-guides root)."""
import json
import os
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent

PY = '''"""Billing service."""


def total(items, vat=0.17):
    """Sum with VAT."""
    s = sum(items)
    return s * (1 + vat)


def _helper():
    return 1


class Invoice(Base):
    """One invoice."""

    def __init__(self, n):
        self.n = n

    def lines(self):
        return []
'''

TS = '''// Price helpers.
export interface Price {
  amount: number;
}

/** Round to agorot. */
export function round2(x: number): number {
  const s = "}";
  return Math.round(x * 100) / 100;
}

export const fmt = (p: Price) => `${p.amount}`;
'''

DART = '''/// A signature stamp.
class Stamp {
  final String name;
  Stamp(this.name);

  String label() {
    setState(() {});
    return "{$name}";
  }
}

int add(int a, int b) {
  return a + b;
}
'''


def make_repo(tmp: Path) -> Path:
    r = tmp / "repo"
    (r / "server" / "app" / "services").mkdir(parents=True)
    (r / "server" / "tests").mkdir()
    (r / "web" / "src").mkdir(parents=True)
    (r / "lib").mkdir()
    (r / "server" / "app" / "services" / "billing.py").write_text(PY)
    (r / "server" / "app" / "__init__.py").write_text("")
    (r / "server" / "tests" / "test_billing.py").write_text("from app.services.billing import total\n")
    (r / "web" / "src" / "price.ts").write_text(TS)
    (r / "web" / "src" / "price.test.ts").write_text("import { round2 } from './price';\n")
    (r / "lib" / "stamp.dart").write_text(DART)
    subprocess.run(["git", "init", "-q"], cwd=r, check=True)
    return r


def run(r: Path, *args, env=None):
    return subprocess.run([sys.executable, str(KIT / "codemap.py"), *args], cwd=r, capture_output=True, text=True,
                          env={**os.environ, **(env or {})}, check=True).stdout


def test_python_exact_ranges_docs_and_tests(tmp_path):
    r = make_repo(tmp_path)
    out = run(r, "outline", "server/app/services/billing.py")
    assert out.startswith("### server/app/services/billing.py · 22 lines · tests: test_billing.py")
    assert "Billing service." in out
    assert "- fn total(items, vat)  L4-7  Sum with VAT." in out
    assert "- fn _helper() (local)  L10-11" in out
    assert "- class Invoice(Base)  L14-21  One invoice." in out
    assert "  - __init__(n)  L17-18" in out and "  - lines()  L20-21" in out


def test_typescript_fallback_braces_in_strings(tmp_path):
    r = make_repo(tmp_path)
    out = run(r, "outline", "web/src/price.ts")
    assert "tests: price.test.ts" in out
    assert "- interface Price  L2-4" in out
    assert "- fn round2(x)  L7-10  Round to agorot." in out  # the "}" inside the string does not end the function
    assert "- fn fmt(p)  L12" in out


def test_dart_classes_members_and_functions(tmp_path):
    r = make_repo(tmp_path)
    out = run(r, "outline", "lib/stamp.dart")
    assert "- class Stamp  L2-10  A signature stamp." in out
    assert "  - label()  L6-9" in out
    assert "setState" not in out  # a call inside a method is not a member
    assert "- fn add(a, b)  L12-14" in out


def test_find_and_write(tmp_path):
    r = make_repo(tmp_path)
    assert "server/app/services/billing.py:4-7  fn total(items, vat)" in run(r, "find", "^total$")
    out = tmp_path / "map"
    run(r, env={"CODEMAP_OUT": str(out)})
    index = (out / "INDEX.md").read_text()
    for f in (p.name for p in out.iterdir() if p.name != "INDEX.md"):
        assert f"| {f} |" in index
    assert "test_billing.py" not in index  # tests are indexed by what they import, not mapped as areas


def test_install_is_idempotent(tmp_path):
    r = make_repo(tmp_path)
    (r / "CLAUDE.md").write_text("# Project\n\nOwn rules.\n")
    for _ in range(2):
        subprocess.run([sys.executable, str(KIT / "install.py"), str(r)], check=True, capture_output=True)
    text = (r / "CLAUDE.md").read_text()
    assert text.startswith("# Project\n\nOwn rules.") and text.count("token-kit:start") == 1
    settings = json.loads((r / ".claude" / "settings.json").read_text())
    assert len(settings["hooks"]["SessionStart"]) == 1
    assert (r / ".gitignore").read_text().count("docs/codemap") == 1
    assert (r / "tools" / "codemap.py").exists() and (r / ".claude" / "hooks" / "session-start.sh").exists()
