import unittest

from mbse_core.module_registry import get_module_entry, get_registered_modules


class ModuleRegistryTests(unittest.TestCase):
    def test_registry_contains_current_domain_modules(self) -> None:
        modules = get_registered_modules()
        module_names = tuple(module.name for module in modules)

        self.assertEqual(module_names, ("initial_sizing", "constraint_analysis"))

    def test_entries_include_required_debug_metadata(self) -> None:
        for module in get_registered_modules():
            self.assertTrue(module.name)
            self.assertTrue(module.package_path)
            self.assertTrue(module.purpose)
            self.assertTrue(module.inputs)
            self.assertTrue(module.outputs)
            self.assertTrue(module.status)

    def test_initial_sizing_connects_to_constraint_analysis(self) -> None:
        initial_sizing = get_module_entry("initial_sizing")

        self.assertEqual(initial_sizing.downstream_modules, ("constraint_analysis",))

    def test_unknown_module_name_raises_key_error(self) -> None:
        with self.assertRaises(KeyError):
            get_module_entry("not_registered")


if __name__ == "__main__":
    unittest.main()
