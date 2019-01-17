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
        for line in file:
            linecount += 1
            if version is None:
                results = fecfile.parse_header(line)
                version = results[1]
            else:
                parsed = fecfile.parse_line(line, version)
                if not parsed:
                    print("** not parsed %s" % line)
                else:
                    # count the form type, if given
                    try:
                        formtypecount.update({parsed['form_type'].upper(): 1})
                    except KeyError:
                        continue

    end = datetime.now()
    print("+++++\nResults:")
    print("\tRan %s rows in %s" % (sum(formtypecount.values()), end-start))
    print("\tTotal rows processed = %s" % formtypecount)


def from_file_speed(filepath, options={}):
    print('++++\nRunning speed test on {0} with {1}'.format(filepath, options))
    start = datetime.now()
    parsed = fecfile.from_file(filepath, options)
    end = datetime.now()
    num_itemizations = 0
    for itemization_type in parsed['itemizations'].keys():
        num_itemizations += len(parsed['itemizations'][itemization_type])
    print('parsed file with {0} itemizations in {1}'.format(
        num_itemizations,
        end - start,
    ))


class SpeedTestSmallFile(unittest.TestCase):
    def test_simple(self):
        speed_test('test-data/1229017.fec')

    def test_from_file(self):
        a_filter = {'filter_itemizations': ['SB']}
        from_file_speed('test-data/1229017.fec', options=a_filter)


class SpeedTestSmallOldFile(unittest.TestCase):
    def test_simple(self):
        speed_test('test-data/27789.fec')

    def test_from_file(self):
        a_filter = {'filter_itemizations': ['SB']}
        from_file_speed('test-data/27789.fec', options=a_filter)


class SpeedTestMediumRecentFile(unittest.TestCase):
    def test_simple(self):
        speed_test('test-data/1162172.fec')

    def test_from_file(self):
        a_filter = {'filter_itemizations': ['SD']}
        from_file_speed('test-data/1162172.fec', options=a_filter)


if __name__ == '__main__':
    regular_tests = unittest.TestSuite([
        SpeedTestSmallFile('test_simple'),
        SpeedTestSmallOldFile('test_simple'),
        SpeedTestMediumRecentFile('test_simple'),
    ])
    from_file_tests = unittest.TestSuite([
        SpeedTestSmallFile('test_from_file'),
        SpeedTestSmallOldFile('test_from_file'),
        SpeedTestMediumRecentFile('test_from_file'),
    ])

    unittest.TextTestRunner().run(from_file_tests)
