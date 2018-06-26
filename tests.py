import unittest
import fecfile
from datetime import datetime
import os
import json
import shutil
import zipfile


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


class HandleF1FromWebForms(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1229011)
        self.assertEqual(parsed['header']['fec_version'], '8.2')
        self.assertEqual(parsed['filing']['treasurer_city'], 'Philadelphia')
        self.assertIsInstance(parsed['filing']['effective_date'], datetime)


class HandlePercentInNumber(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1235309)
        self.assertEqual(parsed['header']['fec_version'], '8.2')
        loan_itemization = parsed['itemizations']['Schedule C'][3]
        self.assertEqual(loan_itemization['loan_interest_rate'], '5.00%')


class HandleNANumber(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1223616)
        self.assertEqual(parsed['filing']['committee_name'], 'Leann for Iowa')
        loan_itemization = parsed['itemizations']['Schedule C'][0]
        self.assertEqual(loan_itemization['loan_interest_rate_terms'], 'N/A')


class ConvertZipFileToJSON(unittest.TestCase):
    def test_convert(self):
        date_str = '20180616'
        z_file = 'test-data/{d}.zip'.format(d=date_str)
        fec_dir = 'test-data/{d}-fec'.format(d=date_str)
        os.mkdir(fec_dir)
        json_dir = 'test-data/{d}-json'.format(d=date_str)
        os.mkdir(json_dir)
        with zipfile.ZipFile(z_file, 'r') as zip_ref:
            zip_ref.extractall(fec_dir)
        files = os.listdir(fec_dir)
        num_files = len(files)
        for f in sorted(files):
            parsed = fecfile.from_file(fec_dir + '/' + f)
            # if type(parsed['filing']['date_signed']) == str:
            #     fecfile.print_example(parsed)
            self.assertIsInstance(parsed['filing']['date_signed'], datetime)
            outpath = json_dir + '/' + f[0:-3] + 'json'
            with open(outpath, 'w') as outf:
                outf.write(
                    json.dumps(parsed, sort_keys=True, indent=2, default=str)
                    )
        new_files = os.listdir(json_dir)
        self.assertEqual(len(new_files), num_files)
        shutil.rmtree(fec_dir)
        shutil.rmtree(json_dir)


if __name__ == '__main__':
    unittest.main()
