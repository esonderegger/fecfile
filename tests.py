import unittest
import fecfile
from datetime import datetime
import os
import json
import shutil
import zipfile
import random
import sys
import warnings


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


class HasScheduleI(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(99840, {'filter_itemizations': ['SI']})
        sched_i = parsed['itemizations']['Schedule I'][0]
        self.assertEqual(sched_i['col_a_subtotal'], 99592.46)


class HandleF1FromWebForms(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1229011)
        self.assertEqual(parsed['header']['fec_version'], '8.2')
        self.assertEqual(parsed['filing']['treasurer_city'], 'Philadelphia')
        self.assertIsInstance(parsed['filing']['effective_date'], datetime)


class HandlePaperF1M(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1101469)
        self.assertEqual(parsed['header']['fec_version'], 'P3.2')
        self.assertEqual(parsed['filing']['city'], 'LUBBOCK')
        self.assertIsInstance(parsed['filing']['date_signed'], datetime)


class HandleSpaceInFormType(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(807197)
        self.assertEqual(parsed['header']['fec_version'], 'P2.6')
        self.assertEqual(parsed['filing']['street_1'], '21 NOB HILL DRIVE')


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


class F99Filing(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1090014)
        self.assertEqual(parsed['header']['fec_version'], '8.1')
        self.assertEqual(
            parsed['filing']['committee_name'],
            'KENT FOR CONGRESS',
        )
        expected = 'Termination of Campaign. Did not exceed $5000 threshold.'
        self.assertEqual(parsed['F99_text'], expected)


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


class SenatePaperFiling(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1226815)
        filing = parsed['filing']
        self.assertEqual(filing['committee_name'], 'FRIENDS OF MARIA')
        first_a = parsed['itemizations']['Schedule A'][0]
        self.assertEqual(first_a['contribution_amount'], 25.0)


class CanParsePaperF3Z(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1160224)
        filing = parsed['filing']
        self.assertEqual(
            filing['committee_name'],
            'BOBBY MAHENDRA FOR SENATE'
            )
        f3z = parsed['itemizations']['F3Z']
        self.assertEqual(f3z[0]['col_a_net_contributions'], 459.75)


class InauguralCommitteeFiling(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1160672)
        filing = parsed['filing']
        comm_name = '58TH PRESIDENTIAL INAUGURAL COMMITTEE'
        self.assertEqual(filing['committee_name'], comm_name)
        first_itemization = parsed['itemizations']['F132'][0]
        self.assertEqual(first_itemization['donation_amount'], 100.0)


class ElectioneeringFiling(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1226989)
        filing = parsed['filing']
        self.assertEqual(filing['organization_name'], '45Committee, Inc.')
        self.assertEqual(filing['total_disbursements'], 56678.84)
        first_91 = parsed['itemizations']['F91'][0]
        self.assertEqual(first_91['controller_city'], 'Herndon')
        first_93 = parsed['itemizations']['F93'][0]
        self.assertEqual(first_93['expenditure_amount'], 48017.00)
        first_94 = parsed['itemizations']['F94'][0]
        self.assertEqual(first_94['candidate_last_name'], 'Manchin')


class Form3SFiling(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1156717)
        summary = parsed['itemizations']['F3S'][0]
        self.assertEqual(summary['a_total_contributions_no_loans'], 11469.22)
        self.assertEqual(summary['total_disbursements'], 55324.77)


class WhiteSpaceNullFields(unittest.TestCase):
    def test_request(self):
        with warnings.catch_warnings(record=True) as w:
            parsed = fecfile.from_http(476351)
            filing = parsed['filing']
            self.assertEqual(filing['report_code'], '12P')
            self.assertEqual(len(w), 0)


class UnnecessaryQuotes(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(1157513)
        filing = parsed['filing']
        comm_name = 'Friends of Dave Brat Inc.'
        self.assertEqual(filing['committee_name'], comm_name)
        first_itemization = parsed['itemizations']['Schedule A'][0]
        self.assertEqual(first_itemization['contribution_amount'], 1500.0)


class V5Filing(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(92888)
        filing = parsed['filing']
        self.assertEqual(
            filing['committee_name'],
            'Mecklenburg County Republican Party'
            )
        sched_b = parsed['itemizations']['Schedule B']
        self.assertEqual(len(sched_b), 5)
        self.assertEqual(sched_b[0]['expenditure_amount'], 500.0)


class V3Filing(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(52888)
        filing = parsed['filing']
        self.assertEqual(
            filing['committee_name'],
            'KEEGAN 2002'
            )
        sched_b = parsed['itemizations']['Schedule B']
        self.assertEqual(len(sched_b), 55)
        self.assertEqual(sched_b[0]['expenditure_amount'], 243.84)


class CommaInCSVFiling(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(22888)
        filing = parsed['filing']
        self.assertEqual(
            filing['committee_name'],
            'PHOENIX FIRE FIGHTERS, LOCAL 493, FIRE PAC COMMITTEE'
            )
        sched_b = parsed['itemizations']['Schedule B']
        self.assertEqual(len(sched_b), 48)
        self.assertEqual(sched_b[0]['expenditure_amount'], 250.0)


class V2Filing(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(12888)
        filing = parsed['filing']
        self.assertEqual(
            filing['committee_name'],
            'Defend America PAC'
            )
        sched_b = parsed['itemizations']['Schedule B']
        self.assertEqual(len(sched_b), 6)
        self.assertEqual(sched_b[0]['expenditure_amount'], 1802.0)


class V1Filing(unittest.TestCase):
    def test_request(self):
        parsed = fecfile.from_http(130)
        filing = parsed['filing']
        self.assertEqual(filing['filer_committee_id_number'], 'C00252791')
        sched_b = parsed['itemizations']['Schedule B']
        self.assertEqual(len(sched_b), 4)
        self.assertEqual(sched_b[0]['expenditure_amount'], 286.61)


class Windows1252Encoding(unittest.TestCase):
    def test_read(self):
        file_path = 'test-data/1260488.fec'
        parsed = fecfile.from_file(file_path)
        self.assertIsInstance(parsed['filing']['date_signed'], datetime)
        self.assertEqual(parsed['filing']['city'], 'Denton')


class OptionsFilterItemizations(unittest.TestCase):
    def test_read(self):
        file_path = 'test-data/1229017.fec'
        a_filter = {'filter_itemizations': ['SB']}
        parsed = fecfile.from_file(file_path, options=a_filter)
        self.assertEqual(parsed['filing']['report_code'], '12P')
        self.assertEqual(len(parsed['itemizations']['Schedule B']), 47)
        self.assertNotIn('Schedule A', parsed['itemizations'])


class ParseHttpIterator(unittest.TestCase):
    def test_parse(self):
        file_num = 1000
        a_filter = {'filter_itemizations': ['SB']}
        items = fecfile.iter_http(file_num, options=a_filter)
        num_itemizations = 0
        for item in items:
            if item.data_type == 'summary':
                self.assertEqual(item.data['report_code'], '12G')
            if item.data_type == 'itemization':
                num_itemizations += 1
        self.assertEqual(num_itemizations, 48)


class ParseFileIterator(unittest.TestCase):
    def test_parse(self):
        file_path = 'test-data/1229017.fec'
        a_filter = {'filter_itemizations': ['SA']}
        items = fecfile.iter_file(file_path, options=a_filter)
        num_itemizations = 0
        for item in items:
            if item.data_type == 'summary':
                self.assertEqual(item.data['report_code'], '12P')
            if item.data_type == 'itemization':
                num_itemizations += 1
        self.assertEqual(num_itemizations, 186)


class AllFormsHaveMappings(unittest.TestCase):
    def test_request(self):
        missing_mappings = {}
        whole_range = list(range(0, 1288000))
        random_sample = random.sample(whole_range, 100)
        for i in random_sample:
            try:
                fecfile.from_http(i)
            except fecfile.FecParserMissingMappingError as ex:
                print(str(i) + ': ' + str(ex))
                relevant_str = str(ex)[13:].split(' - ')[0]
                if relevant_str in missing_mappings:
                    missing_mappings[relevant_str] += 1
                else:
                    missing_mappings[relevant_str] = 1
        for m in sorted(missing_mappings.keys()):
            print('{a} ({b})'.format(a=m, b=missing_mappings[m]))
        self.assertEqual(len(missing_mappings.keys()), 0)


if __name__ == '__main__':
    regular_tests = unittest.TestSuite([
        CandidateTest('test_simple'),
        PacViaHttpRequest('test_request'),
        TextLastRow('test_request'),
        IndependentExpendituresReport('test_request'),
        HasScheduleC('test_request'),
        HasScheduleD('test_request'),
        HasScheduleI('test_request'),
        HandleF1FromWebForms('test_request'),
        HandlePaperF1M('test_request'),
        HandleSpaceInFormType('test_request'),
        HandlePercentInNumber('test_request'),
        HandleNANumber('test_request'),
        F99Filing('test_request'),
        ConvertZipFileToJSON('test_convert'),
        SenatePaperFiling('test_request'),
        CanParsePaperF3Z('test_request'),
        InauguralCommitteeFiling('test_request'),
        ElectioneeringFiling('test_request'),
        Form3SFiling('test_request'),
        WhiteSpaceNullFields('test_request'),
        UnnecessaryQuotes('test_request'),
        V5Filing('test_request'),
        V3Filing('test_request'),
        CommaInCSVFiling('test_request'),
        V2Filing('test_request'),
        V1Filing('test_request'),
        Windows1252Encoding('test_read'),
        OptionsFilterItemizations('test_read'),
        ParseHttpIterator('test_parse'),
        ParseFileIterator('test_parse'),
    ])
    mappings_test = unittest.TestSuite([AllFormsHaveMappings('test_request')])
    if len(sys.argv) > 1 and sys.argv[1] == 'mappings':
        unittest.TextTestRunner().run(mappings_test)
    else:
        unittest.TextTestRunner().run(regular_tests)
