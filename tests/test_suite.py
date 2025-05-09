import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.associations import AssociationTest
from tests.event import EventTest
from tests.pass_ import PassTest
from tests.support_ticket import SupportTicketTest
from tests.team import TeamTest
from tests.user import UserTest


def create_suite() -> unittest.TestSuite:
    """Creates a test suite for the entire project."""
    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EventTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(PassTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SupportTicketTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TeamTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(UserTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(AssociationTest))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(create_suite())
