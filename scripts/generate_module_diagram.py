"""Generate the current module map as Mermaid Markdown."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mbse_core.module_graph import write_mermaid_module_graph


OUTPUT_PATH = Path("docs/diagrams/current_module_map.md")


def main() -> None:
    output_path = write_mermaid_module_graph(OUTPUT_PATH)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
