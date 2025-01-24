import unittest

from tests.pass_ import PassTest


def create_suite() -> unittest.TestSuite:
    """Creates a test suite for the entire project."""
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(PassTest))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(create_suite())
