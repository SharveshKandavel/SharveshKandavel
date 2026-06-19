#!/usr/bin/env python3
"""
generate_readme.py
Generates the dynamic sections of README.md and injects them.
Run via GitHub Actions daily to keep the README fresh.
"""

import os
import re
import sys
from datetime import datetime, timezone

# ─── Timestamp block ────────────────────────────────────────────────────────

def get_timestamp() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%B %d, %Y at %H:%M UTC")

# ─── Inject into README ──────────────────────────────────────────────────────

def inject_section(readme: str, tag: str, content: str) -> str:
    """Replace content between <!-- START:tag --> and <!-- END:tag --> markers."""
    pattern = rf"<!-- START:{tag} -->.*?<!-- END:{tag} -->"
    replacement = f"<!-- START:{tag} -->\n{content}\n<!-- END:{tag} -->"
    return re.sub(pattern, replacement, readme, flags=re.DOTALL)

def main():
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")

    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    # Inject last-updated timestamp
    timestamp_content = (
        f"> 🕐 **Last updated:** {get_timestamp()}  \n"
        f"> *Auto-refreshed daily by [GitHub Actions](../../actions)*"
    )
    readme = inject_section(readme, "TIMESTAMP", timestamp_content)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme)

    sys.stdout.buffer.write(f"[OK] README updated at {get_timestamp()}\n".encode("utf-8"))

if __name__ == "__main__":
    main()
