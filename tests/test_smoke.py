import importlib
import unittest


class InitialPackageSmokeTest(unittest.TestCase):
    def test_initial_packages_import(self) -> None:
        package_names = [
            "mbse_core",
            "domains",
            "domains.aerodynamics",
            "domains.constraint_analysis",
            "domains.geometry",
            "domains.initial_sizing",
            "domains.mission",
            "domains.performance",
            "domains.propulsion",
            "domains.stability_control",
            "domains.structures",
            "domains.weights",
        ]

        for package_name in package_names:
            self.assertIsNotNone(importlib.import_module(package_name))
