"""Terminal and Mermaid renderers for the registered module map."""

from __future__ import annotations

from collections.abc import Iterable
from importlib import import_module
from pathlib import Path

from mbse_core.module_registry import ModuleEntry, get_registered_modules


def render_ascii_module_graph(modules: Iterable[ModuleEntry] | None = None) -> str:
    """Return a node-style terminal view of modules and directed connections."""

    module_entries = tuple(modules) if modules is not None else get_registered_modules()
    lines = ["Module Node Graph", "=================", ""]

    for module in module_entries:
        lines.extend(_ascii_module_box(module))
        lines.append("")

    lines.extend(["Connections", "-----------"])
    connection_lines = _connection_lines(module_entries)
    lines.extend(connection_lines if connection_lines else ["(none)"])
    return "\n".join(lines).rstrip() + "\n"


def render_mermaid_module_graph(modules: Iterable[ModuleEntry] | None = None) -> str:
    """Return a Markdown document containing the current node-style module map."""

    module_entries = tuple(modules) if modules is not None else get_registered_modules()
    lines = [
        "# Current Module Map",
        "",
        "Generated from `mbse_core.module_registry`.",
        "",
        "## Mermaid Diagram",
        "",
        "```mermaid",
        "flowchart LR",
    ]

    for module in module_entries:
        lines.extend(_mermaid_module_node_lines(module))

    for module in module_entries:
        for downstream in module.downstream_modules:
            lines.append(
                f"    {module.name}_outputs -->|downstream| {downstream}_inputs"
            )

    lines.extend(["```", ""])
    lines.extend(_module_detail_lines(module_entries))
    lines.extend(_regeneration_lines())
    return "\n".join(lines).rstrip() + "\n"


def write_mermaid_module_graph(
    output_path: str | Path, modules: Iterable[ModuleEntry] | None = None
) -> Path:
    """Write the Mermaid Markdown module graph and return the output path."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_mermaid_module_graph(modules), encoding="utf-8")
    return path


def inspect_public_exports(modules: Iterable[ModuleEntry] | None = None) -> str:
    """Return importable public exports for each registered module package."""

    module_entries = tuple(modules) if modules is not None else get_registered_modules()
    lines = ["Module Interface Exports", "========================", ""]

    for module_entry in module_entries:
        lines.append(f"[{module_entry.name}]")
        lines.append(f"  package: {module_entry.package_path}")
        try:
            imported_module = import_module(module_entry.package_path)
        except ImportError as exc:
            lines.append(f"  import_error: {exc}")
            lines.append("")
            continue

        exports = getattr(imported_module, "__all__", None)
        if exports is None:
            public_names = tuple(
                name for name in dir(imported_module) if not name.startswith("_")
            )
        else:
            public_names = tuple(str(name) for name in exports)

        if public_names:
            lines.append("  exports:")
            lines.extend(_bullet_lines(public_names, indent="    - "))
        else:
            lines.append("  exports: (none)")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _bullet_lines(values: Iterable[str], indent: str) -> list[str]:
    return [f"{indent}{value}" for value in values]


def _ascii_module_box(module: ModuleEntry) -> list[str]:
    input_lines = [f"o {value}" for value in module.inputs]
    body_lines = [
        module.name,
        f"package: {module.package_path}",
        f"status: {module.status}",
        f"purpose: {module.purpose}",
    ]
    output_lines = [f"o {value}" for value in module.outputs]

    input_width = max(len("INPUTS"), *(len(line) for line in input_lines))
    body_width = max(len("MODULE"), *(len(line) for line in body_lines))
    output_width = max(len("OUTPUTS"), *(len(line) for line in output_lines))
    total_width = input_width + body_width + output_width + 10
    border = "+" + "-" * total_width + "+"
    separator = (
        "+"
        + "-" * (input_width + 2)
        + "+"
        + "-" * (body_width + 2)
        + "+"
        + "-" * (output_width + 2)
        + "+"
    )

    lines = [
        border,
        _ascii_row("INPUTS", "MODULE", "OUTPUTS", input_width, body_width, output_width),
        separator,
    ]
    row_count = max(len(input_lines), len(body_lines), len(output_lines))
    for index in range(row_count):
        input_value = input_lines[index] if index < len(input_lines) else ""
        body_value = body_lines[index] if index < len(body_lines) else ""
        output_value = output_lines[index] if index < len(output_lines) else ""
        lines.append(
            _ascii_row(
                input_value,
                body_value,
                output_value,
                input_width,
                body_width,
                output_width,
            )
        )
    lines.append(separator)

    downstream = ", ".join(module.downstream_modules) or "(none)"
    lines.append(f"downstream: {downstream}")
    return lines


def _ascii_row(
    left: str,
    center: str,
    right: str,
    left_width: int,
    center_width: int,
    right_width: int,
) -> str:
    return (
        f"| {left:<{left_width}} "
        f"| {center:<{center_width}} "
        f"| {right:<{right_width}} |"
    )


def _connection_lines(modules: Iterable[ModuleEntry]) -> list[str]:
    lines: list[str] = []
    for module in modules:
        for downstream in module.downstream_modules:
            lines.append(f"{module.name} -> {downstream}")
    return lines


def _mermaid_module_node_lines(module: ModuleEntry) -> list[str]:
    lines = [
        f'    subgraph {module.name}_node["{module.name}"]',
        "        direction LR",
    ]
    lines.append(f'        {module.name}_inputs["Inputs"]')
    for index, input_name in enumerate(module.inputs, start=1):
        lines.append(f'        {module.name}_in_{index}["{input_name}"]')
        lines.append(f"        {module.name}_in_{index} --> {module.name}_inputs")
    lines.append(
        f'        {module.name}_body["{module.name}<br/>{module.status}<br/>{module.package_path}"]'
    )
    lines.append(f'        {module.name}_outputs["Outputs"]')
    for index, output_name in enumerate(module.outputs, start=1):
        lines.append(f'        {module.name}_out_{index}["{output_name}"]')
        lines.append(f"        {module.name}_outputs --> {module.name}_out_{index}")
    lines.extend(
        [
            f"        {module.name}_inputs --> {module.name}_body",
            f"        {module.name}_body --> {module.name}_outputs",
            "    end",
        ]
    )
    return lines


def _module_detail_lines(modules: Iterable[ModuleEntry]) -> list[str]:
    lines = ["## Registered Modules", ""]
    for module in modules:
        downstream = ", ".join(module.downstream_modules) or "(none)"
        lines.extend(
            [
                f"### {module.name}",
                "",
                f"- Package: `{module.package_path}`",
                f"- Status: `{module.status}`",
                f"- Purpose: {module.purpose}",
                f"- Inputs: {', '.join(module.inputs)}",
                f"- Outputs: {', '.join(module.outputs)}",
                f"- Downstream modules: {downstream}",
                "",
            ]
        )
    return lines


def _regeneration_lines() -> list[str]:
    return [
        "## Regenerating This Diagram",
        "",
        "From the repository root, run:",
        "",
        "```bash",
        "python3 scripts/generate_module_diagram.py",
        "```",
        "",
        "The script reads `mbse_core.module_registry` as the source of truth and rewrites this Markdown file.",
        "",
    ]


__all__ = [
    "inspect_public_exports",
    "render_ascii_module_graph",
    "render_mermaid_module_graph",
    "write_mermaid_module_graph",
]
