"""Print public exports for each registered module package."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mbse_core.module_graph import inspect_public_exports


def main() -> None:
    print(inspect_public_exports(), end="")


if __name__ == "__main__":
    main()
