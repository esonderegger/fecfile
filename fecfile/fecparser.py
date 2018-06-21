from datetime import datetime
from pytz import timezone
import json
import os
import re


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
    for i in range(len(lines)):
        line = lines[i]
        parsed = parseline(line, version)
        if parsed and 'fec_version' in parsed:
            version = parsed['fec_version']
            out['header'] = parsed
        elif i < 2:
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


def parseline(line, version):
    fields = line.split(chr(0x1c))
    for mapping in mappings.keys():
        form = fields[0]
        if re.match(mapping, form, re.IGNORECASE):
            versions = mappings[mapping].keys()
            for v in versions:
                ver = version if version else fields[2]
                if re.match(v, ver, re.IGNORECASE):
                    out = {}
                    for i in range(len(mappings[mapping][v])):
                        val = fields[i] if i < len(fields) else ''
                        k = mappings[mapping][v][i]
                        out[k] = getTyped(form, ver, k, val)
                    return out
    return None


def getTyped(form, version, field, value):
    for mapping in types.keys():
        if re.match(mapping, form, re.IGNORECASE):
            versions = types[mapping].keys()
            for v in versions:
                if re.match(v, version, re.IGNORECASE):
                    properties = types[mapping][v]
                    prop_keys = properties.keys()
                    for prop_key in prop_keys:
                        if re.match(prop_key, field, re.IGNORECASE):
                            property = properties[prop_key]
                            if property['type'] == 'integer':
                                return int(value)
                            if property['type'] == 'float':
                                if value == '' or value.lower() == 'none':
                                    return None
                                return float(value)
                            if property['type'] == 'date':
                                format = property['format']
                                if value == '':
                                    return None
                                parsed_date = datetime.strptime(value, format)
                                return eastern.localize(parsed_date)
    return value


def print_example(parsed):
    out = {'filing': parsed['filing'], 'itemizations': {}}
    for k in parsed['itemizations'].keys():
        out['itemizations'][k] = parsed['itemizations'][k][0]
    print(json.dumps(out, sort_keys=True, indent=2, default=str))
