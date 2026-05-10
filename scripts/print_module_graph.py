"""Print the current registered module graph as plain text."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mbse_core.module_graph import render_ascii_module_graph


def main() -> None:
    print(render_ascii_module_graph(), end="")


if __name__ == "__main__":
    main()
