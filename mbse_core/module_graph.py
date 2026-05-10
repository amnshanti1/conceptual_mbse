"""Terminal and Mermaid renderers for the registered module map."""

from __future__ import annotations

from collections.abc import Iterable
from importlib import import_module
from pathlib import Path

from mbse_core.module_registry import ModuleEntry, get_registered_modules


def render_ascii_module_graph(modules: Iterable[ModuleEntry] | None = None) -> str:
    """Return a readable terminal view of modules and directed connections."""

    module_entries = tuple(modules) if modules is not None else get_registered_modules()
    lines = ["Module Graph", "============", ""]

    for module in module_entries:
        downstream = ", ".join(module.downstream_modules) or "(none)"
        lines.extend(
            [
                f"[{module.name}]",
                f"  package: {module.package_path}",
                f"  status: {module.status}",
                f"  purpose: {module.purpose}",
                "  inputs:",
                *_bullet_lines(module.inputs, indent="    - "),
                "  outputs:",
                *_bullet_lines(module.outputs, indent="    - "),
                f"  downstream: {downstream}",
                "",
            ]
        )

    lines.extend(["Connections", "-----------"])
    connection_lines = _connection_lines(module_entries)
    lines.extend(connection_lines if connection_lines else ["(none)"])
    return "\n".join(lines).rstrip() + "\n"


def render_mermaid_module_graph(modules: Iterable[ModuleEntry] | None = None) -> str:
    """Return a Markdown document containing the current module map."""

    module_entries = tuple(modules) if modules is not None else get_registered_modules()
    lines = [
        "# Current Module Map",
        "",
        "Generated from `mbse_core.module_registry`.",
        "",
        "```mermaid",
        "flowchart LR",
    ]

    for module in module_entries:
        label = _mermaid_label(module)
        lines.append(f'    {module.name}["{label}"]')

    for module in module_entries:
        for downstream in module.downstream_modules:
            lines.append(f"    {module.name} --> {downstream}")

    lines.extend(["```", ""])
    lines.extend(_module_detail_lines(module_entries))
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


def _connection_lines(modules: Iterable[ModuleEntry]) -> list[str]:
    lines: list[str] = []
    for module in modules:
        for downstream in module.downstream_modules:
            lines.append(f"{module.name} -> {downstream}")
    return lines


def _mermaid_label(module: ModuleEntry) -> str:
    inputs = "<br/>".join(f"in: {value}" for value in module.inputs)
    outputs = "<br/>".join(f"out: {value}" for value in module.outputs)
    return "<br/>".join(
        (
            module.name,
            module.status,
            inputs,
            outputs,
        )
    )


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


__all__ = [
    "inspect_public_exports",
    "render_ascii_module_graph",
    "render_mermaid_module_graph",
    "write_mermaid_module_graph",
]
