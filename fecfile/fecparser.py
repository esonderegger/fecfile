from datetime import datetime
from pytz import timezone
import csv
import json
import os
import re
import warnings


class FecParserTypeWarning(UserWarning):
    """when data in an FEC filing doesn't match types.json"""
    pass


class FecParserMissingMappingError(Exception):
    """when a line in an FEC filing doesn't have a form/version mapping"""
    def __init__(self, opts, msg=None):
        if msg is None:
            msg = ('cannot parse version {v} of form {f} - '
                   'no mapping found').format(
                v=opts['version'],
                f=opts['form'],
            )
        super(FecParserMissingMappingError, self).__init__(msg)


this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
mappings_file = os.path.join(this_dir, 'mappings.json')
types_file = os.path.join(this_dir, 'types.json')
mappings = {}
types = {}
with open(mappings_file) as data_file:
    mappings = json.loads(data_file.read())
with open(types_file) as data_file:
    types = json.loads(data_file.read())
eastern = timezone('US/Eastern')


def loads(input):
    version = None
    lines = input.split('\n')
    out = {'itemizations': {}, 'text': [], 'header': {}, 'filing': {}}
    out['header'], version, header_length = parse_header(lines)
    for i in range(header_length, len(lines)):
        line = lines[i]
        parsed = parseline(line, version, i)
        if i < header_length + 1:
            out['filing'] = parsed
        elif parsed:
            if 'form_type' in parsed:
                form_type = parsed['form_type']
                if form_type[0] == 'S':
                    form_type = 'Schedule ' + parsed['form_type'][1]
                if form_type in out['itemizations']:
                    out['itemizations'][form_type].append(parsed)
                else:
                    out['itemizations'][form_type] = [parsed]
            else:
                out['text'].append(parsed)
    return out


def fields_from_line(line):
    if chr(0x1c) in line:
        fields = line.split(chr(0x1c))
    else:
        reader = csv.reader([line])
        fields = next(reader)
    for field in fields:
        if field.startswith('"') and field.endswith('"'):
            field = field[1:-1]
    return list(map(
        lambda x: x[1:-1] if (x.startswith('"') and x.endswith('"')) else x,
        fields
    ))


def parse_header(lines):
    if lines[0].startswith('/*'):
        header_size = 1
        header = {'schedule_counts': {}}
        schedule_counts = False
        while not lines[header_size].startswith('/*'):
            this_line = lines[header_size]
            if this_line.lower().startswith('schedule_counts'):
                schedule_counts = True
            else:
                header_fields = this_line.split('=')
                k = header_fields[0].strip().lower()
                v = header_fields[1].strip().lower()
                if schedule_counts:
                    header['schedule_counts'][k] = int(v)
                else:
                    header[k] = v
            header_size += 1
        return header, header['fec_ver_#'], header_size + 1
    fields = fields_from_line(lines[0])
    if fields[1] == 'FEC':
        parsed = parseline(lines[0], fields[2], 0)
        return parsed, fields[2], 1
    parsed = parseline(lines[0], fields[1], 0)
    return parsed, fields[1], 1


def parseline(line, version, line_num):
    fields = fields_from_line(line)
    if len(fields) < 2:
        return None
    for mapping in mappings.keys():
        form = fields[0]
        if re.match(mapping, form, re.IGNORECASE):
            versions = mappings[mapping].keys()
            for v in versions:
                if re.match(v, version, re.IGNORECASE):
                    out = {}
                    for i in range(len(mappings[mapping][v])):
                        val = fields[i] if i < len(fields) else ''
                        k = mappings[mapping][v][i]
                        out[k] = getTyped(form, version, k, val, line_num)
                    return out
    raise FecParserMissingMappingError({
        'form': form,
        'version': version,
    })


nones = ['none', 'n/a']


def getTyped(form, version, field, value, line_num):
    for mapping in types.keys():
        if re.match(mapping, form, re.IGNORECASE):
            versions = types[mapping].keys()
            for v in versions:
                if re.match(v, version, re.IGNORECASE):
                    properties = types[mapping][v]
                    prop_keys = properties.keys()
                    for prop_key in prop_keys:
                        if re.match(prop_key, field, re.IGNORECASE):
                            prop = properties[prop_key]
                            try:
                                if prop['type'] == 'integer':
                                    return int(value)
                                if prop['type'] == 'float':
                                    if value == '' or value.lower() in nones:
                                        return None
                                    sanitized = value.replace('%', '')
                                    return float(sanitized)
                                if prop['type'] == 'date':
                                    format = prop['format']
                                    if value == '':
                                        return None
                                    parsed_date = datetime.strptime(
                                        value,
                                        format)
                                    return eastern.localize(parsed_date)
                            except ValueError:
                                warnings.warn(
                                    'cannot parse value: {v}, as type: {t}, '
                                    'for field: {f}, in form: {o}, '
                                    'version: {r} (line {n})'.format(
                                        v=value,
                                        t=prop['type'],
                                        f=field,
                                        o=form,
                                        r=version,
                                        n=line_num + 1,
                                    ),
                                    FecParserTypeWarning,
                                )
                                return None
    return value


def print_example(parsed):
    out = {'filing': parsed['filing'], 'itemizations': {}}
    for k in parsed['itemizations'].keys():
        out['itemizations'][k] = parsed['itemizations'][k][0]
    print(json.dumps(out, sort_keys=True, indent=2, default=str))
