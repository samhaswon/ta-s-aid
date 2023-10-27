from unittest import TestCase
from modules.unit_test import UnitTest


class TestUnitTest(TestCase):
    def test_do_tests(self):
        with open("ids.txt", "r") as student_file:
            student_list = student_file.read().splitlines()
        unit_test = UnitTest(student_list, "test_destination")
        unit_test.do_tests()
