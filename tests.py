import unittest
import requests
import fecfile


class CandidateTest(unittest.TestCase):
    def test_simple(self):
        parsed = {}
        with open('test-data/1229017.fec') as file:
            unparsed = file.read()
            parsed = fecfile.loads(unparsed)
        self.assertEqual(parsed['report_code'], '12P')
        self.assertEqual(parsed['col_a_cash_on_hand_close'], 1141844.62)
        self.assertEqual(len(parsed['itemizations']['Schedule A']), 186)
        self.assertEqual(len(parsed['itemizations']['Schedule B']), 47)


class PacViaHttpRequest(unittest.TestCase):
    def test_request(self):
        url = 'http://docquery.fec.gov/dcdev/posted/1232195.fec'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        parsed = fecfile.loads(r.text)
        self.assertEqual(parsed['report_code'], 'M5')
        self.assertEqual(parsed['state'], 'DC')
        self.assertEqual(len(parsed['itemizations']['Schedule A']), 5)
        self.assertEqual(len(parsed['itemizations']['Schedule B']), 8)


class TextLastRow(unittest.TestCase):
    def test_request(self):
        url = 'http://docquery.fec.gov/dcdev/posted/1232188.fec'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        parsed = fecfile.loads(r.text)
        self.assertEqual(parsed['report_code'], 'M5')
        self.assertEqual(parsed['state'], 'NJ')
        self.assertEqual(len(parsed['itemizations']['Schedule A']), 1)
        self.assertEqual(len(parsed['itemizations']['Schedule B']), 11)
        self.assertEqual(len(parsed['text']), 1)


class IndependentExpendituresReport(unittest.TestCase):
    def test_request(self):
        url = 'http://docquery.fec.gov/dcdev/posted/1146148.fec'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        parsed = fecfile.loads(r.text)
        self.assertEqual(parsed['report_code'], 'YE')
        self.assertEqual(parsed['state'], 'DC')
        self.assertEqual(len(parsed['itemizations']['F57']), 5)


if __name__ == '__main__':
    unittest.main()
