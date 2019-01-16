import unittest
from datetime import datetime
import fecfile

from collections import Counter


def speed_test(filepath):
    print("+++++\nRunning speed test on %s" % filepath)
    formtypecount = Counter()

    start = datetime.now()
    parsed = {}
    with open(filepath) as file:
        linecount = 0
        version = None
        header = None
        for line in file:
            linecount+=1
            if version is None:
                results = fecfile.parse_header(line)
                header = results[0]
                version = results[1]
            else:
                parsed = fecfile.parse_line(line, version)
            
                if not parsed:
                    print("** not parsed %s" % line)
                else:   
                    # count the form type, if given
                    try:
                        formtypecount.update({parsed['form_type'].upper():1})
                    except KeyError:
                        continue

    end = datetime.now()
    print("+++++\nResults:")
    print("\tRan %s rows in %s" % (sum(formtypecount.values()), end-start))
    print("\tTotal rows processed = %s" % formtypecount)


class SpeedTestSmallFile(unittest.TestCase):
    def test_simple(self):
        speed_test('test-data/1229017.fec')


class SpeedTestSmallOldFile(unittest.TestCase):
    def test_simple(self):
        speed_test('test-data/27789.fec')

class SpeedTestMediumRecentFile(unittest.TestCase):
    def test_simple(self):
        speed_test('test-data/1162172.fec')



if __name__ == '__main__':
    regular_tests = unittest.TestSuite([
        SpeedTestSmallFile('test_simple'),
        SpeedTestSmallOldFile('test_simple'),
        SpeedTestMediumRecentFile('test_simple'),

    ])

    unittest.TextTestRunner().run(regular_tests)

