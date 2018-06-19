import unittest
from fecfile import parse


class CandidateTest(unittest.TestCase):
    def test_simple(self):
        parsed = {}
        with open('test-data/1229017.fec') as file:
            unparsed = file.read()
            parsed = parse(unparsed)
        self.assertEqual(parsed['report_code'], '12P')
        self.assertEqual(parsed['col_a_cash_on_hand_close'], '1141844.62')
        self.assertEqual(len(parsed['itemizations']['Schedule A']), 186)
        self.assertEqual(len(parsed['itemizations']['Schedule B']), 47)


if __name__ == '__main__':
    unittest.main()
