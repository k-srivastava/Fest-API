import unittest

from tests.event import EventTest
from tests.pass_ import PassTest
from tests.team import TeamTest
from tests.user import UserTest


def create_suite() -> unittest.TestSuite:
    """Creates a test suite for the entire project."""
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(EventTest))
    suite.addTest(unittest.makeSuite(PassTest))
    suite.addTest(unittest.makeSuite(TeamTest))
    suite.addTest(unittest.makeSuite(UserTest))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(create_suite())
