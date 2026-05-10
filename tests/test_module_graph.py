import tempfile
import unittest
from pathlib import Path

from mbse_core.module_graph import (
    inspect_public_exports,
    render_ascii_module_graph,
    render_mermaid_module_graph,
    write_mermaid_module_graph,
)


class ModuleGraphTests(unittest.TestCase):
    def test_ascii_graph_includes_modules_and_connection(self) -> None:
        output = render_ascii_module_graph()

        self.assertIn("Module Node Graph", output)
        self.assertIn("| INPUTS", output)
        self.assertIn("| MODULE", output)
        self.assertIn("| OUTPUTS", output)
        self.assertIn("initial_sizing", output)
        self.assertIn("constraint_analysis", output)
        self.assertIn("initial_sizing -> constraint_analysis", output)
        self.assertIn("o InitialSizingInputs", output)
        self.assertIn("o ConstraintAnalysisOutputs", output)

    def test_mermaid_graph_includes_node_ports_and_connection(self) -> None:
        output = render_mermaid_module_graph()

        self.assertIn("```mermaid", output)
        self.assertIn("flowchart LR", output)
        self.assertIn('subgraph initial_sizing_node["initial_sizing"]', output)
        self.assertIn('initial_sizing_inputs["Inputs"]', output)
        self.assertIn('initial_sizing_body["initial_sizing', output)
        self.assertIn('initial_sizing_outputs["Outputs"]', output)
        self.assertIn("initial_sizing_outputs -->|downstream| constraint_analysis_inputs", output)
        self.assertIn("## Registered Modules", output)
        self.assertIn("## Regenerating This Diagram", output)

    def test_write_mermaid_graph_creates_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "nested" / "module_map.md"

            returned_path = write_mermaid_module_graph(output_path)

            self.assertEqual(returned_path, output_path)
            self.assertTrue(output_path.exists())
            self.assertIn("Current Module Map", output_path.read_text(encoding="utf-8"))

    def test_inspect_public_exports_reads_registered_packages(self) -> None:
        output = inspect_public_exports()

        self.assertIn("[initial_sizing]", output)
        self.assertIn("run_initial_sizing", output)
        self.assertIn("[constraint_analysis]", output)
        self.assertIn("run_constraint_analysis", output)


if __name__ == "__main__":
    unittest.main()
