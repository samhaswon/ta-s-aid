from unittest import TestCase
from modules.import_check import ImportCheck
import os


class TestImportCheck(TestCase):
    def test_check(self):
        folders = [x[1] for x in os.walk("imports")][0]
        for folder in folders:
            with open(f"imports{os.path.sep + folder}.txt", "w") as test_file:
                test_file.write("Some output\n")
        import_check = ImportCheck("imports")
        import_check.check("file.py", "random")

        # Test to see that Jeffs A and B did import random
        with open(f"imports{os.path.sep}Jeff A.txt", "r") as jeff_file:
            self.assertNotIn("You did not import (and therefore did not use) random",
                             jeff_file.read())
        with open(f"imports{os.path.sep}Jeff B.txt", "r") as jeff_file:
            self.assertNotIn("You did not import (and therefore did not use) random",
                             jeff_file.read())

        # Test to see that Jeffs C and D didn't import random
        with open(f"imports{os.path.sep}Jeff C.txt", "r") as jeff_file:
            self.assertIn("You did not import (and therefore did not use) random",
                          jeff_file.read())
        with open(f"imports{os.path.sep}Jeff D.txt", "r") as jeff_file:
            self.assertIn("You did not import (and therefore did not use) random",
                          jeff_file.read())
