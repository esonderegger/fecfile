from . import fecparser
import requests


FecParserMissingMappingError = fecparser.FecParserMissingMappingError


def loads(input):
    """Deserialize ``input`` (a ``str`` instance
    containing an FEC document) to a Python object.
    """
    return fecparser.loads(input)


def parse_header(hdr):
    """Deserialize a ``str`` or a list of ``str`` instances containing
    header information for an FEC document. Returns an Python object, the
    version ``str`` used in the document, and the number of lines used
    by the header.

    The third return value of number of lines used by the header is only
    useful for versions 1 and 2 of the FEC file format, when the header
    was a multiline string beginning and ending with ``/*``. This allows
    us to pass in the entire contents of the file as a list of lines and
    know where to start parsing the non-header lines.
    """
    if type(hdr) is list:
        return fecparser.parse_header(hdr)
    else:
        return fecparser.parse_header([hdr])


def parse_line(line, version, line_num=None):
    """Deserialize a ``line`` (a ``str`` instance
    containing a line from an FEC document) to a Python object.

    ``version`` is a ``str`` instance for the version of the FEC file format
    to be used, and is required.

    ``line_num`` is optional and is used for debugging. If an error or
    warning is encountered, whatever is passed in to ``line_num`` will be
    included in the error/warning message.
    """
    return fecparser.parse_line(line, version, line_num)


def from_http(file_number):
    """Utility method for getting a parsed Python representation of an FEC
    filing when you don't already have it on your computer. This method takes
    either a ``str`` or ``int`` as a ``file_number`` and requests it from
    the ``docquery.fec.gov`` server, then parses the response.
    """
    url = 'http://docquery.fec.gov/dcdev/posted/{n}.fec'.format(n=file_number)
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 404:
        url = 'http://docquery.fec.gov/paper/posted/{n}.fec'.format(
            n=file_number
        )
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 404:
        return None
    return fecparser.loads(r.text)


def from_file(file_path):
    """Utility method for getting a parsed Python representation of an FEC
    filing when you have the .fec file on your computer. This method takes
    a ``str`` of the path to the file, and returns the parsed Python object.
    """
    parsed = {}
    with open(file_path) as file:
        unparsed = file.read()
        parsed = fecparser.loads(unparsed)
    return parsed


def print_example(parsed):
    """Utility method for debugging - prints out a representative subset of
    the Python object returned by one of the deserialization methods. For
    filings with itemizations, it only prints the first of each type of
    itemization included in the object.
    """
    fecparser.print_example(parsed)
