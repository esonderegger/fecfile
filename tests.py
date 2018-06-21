import unittest
import fecfile
from datetime import datetime


class CandidateTest(unittest.TestCase):
    def test_simple(self):
        parsed = {}
        with open('test-data/1229017.fec') as file:
            unparsed = file.read()
            parsed = fecfile.loads(unparsed)
        self.assertEqual(parsed['filing']['report_code'], '12P')
        filing = parsed['filing']
        self.assertEqual(filing['col_a_cash_on_hand_close'], 1141844.62)
        self.assertIsInstance(filing['date_signed'], datetime)
        self.assertEqual(len(parsed['itemizations']['Schedule A']), 186)
        self.assertEqual(len(parsed['itemizations']['Schedule B']), 47)


class PacViaHttpRequest(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1232195)
        self.assertEqual(parsed['filing']['report_code'], 'M5')
        self.assertEqual(parsed['filing']['state'], 'DC')
        self.assertEqual(len(parsed['itemizations']['Schedule A']), 5)
        self.assertEqual(len(parsed['itemizations']['Schedule B']), 8)


class TextLastRow(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1232188)
        self.assertEqual(parsed['filing']['report_code'], 'M5')
        self.assertEqual(parsed['filing']['state'], 'NJ')
        self.assertEqual(len(parsed['itemizations']['Schedule A']), 1)
        self.assertEqual(len(parsed['itemizations']['Schedule B']), 11)
        self.assertEqual(len(parsed['text']), 1)


class IndependentExpendituresReport(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1146148)
        self.assertEqual(parsed['filing']['report_code'], 'YE')
        self.assertEqual(parsed['filing']['state'], 'DC')
        self.assertEqual(len(parsed['itemizations']['F57']), 5)


class HasScheduleC(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1229012)
        sched_c = parsed['itemizations']['Schedule C'][0]
        self.assertEqual(sched_c['loan_balance'], 30000.00)


class HasScheduleD(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1146147)
        sched_d = parsed['itemizations']['Schedule D'][0]
        self.assertEqual(sched_d['balance_at_close_this_period'], 26622.00)


if __name__ == '__main__':
    unittest.main()
