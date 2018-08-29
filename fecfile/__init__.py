from . import fecparser
import requests


FecParserMissingMappingError = fecparser.FecParserMissingMappingError


def loads(input):
    return fecparser.loads(input)


def from_http(file_number):
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
    parsed = {}
    with open(file_path) as file:
        unparsed = file.read()
        parsed = fecparser.loads(unparsed)
    return parsed


def print_example(parsed):
    fecparser.print_example(parsed)
