import unittest
from conveyr import Conveyor


class ConveyrTest(unittest.TestCase):
    def test_1(self):

        conveyr = Conveyor()
        self.assertIsNotNone(conveyr)
