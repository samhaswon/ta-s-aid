from unittest import TestCase
from modules.unit_test import UnitTest
import os


class TestUnitTest(TestCase):
    def test_do_tests(self):
        try:
            with open("ids.txt", "r") as student_file:
                student_list = student_file.read().splitlines()
            unit_test = UnitTest("test_destination")
            unit_test.do_tests()
            self.assertEqual(len(student_list), len([x[2] for x in os.walk("test_destination")][0]))
        except Exception as e:
            self.fail(f"Failure: \n\n{e}")
