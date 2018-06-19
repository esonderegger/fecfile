import json
import os
import re


this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
mappings_file = os.path.join(this_dir, 'mappings.json')
mappings = {}
with open(mappings_file) as data_file:
    mappings = json.loads(data_file.read())


def parse(input):
    version = None
    lines = input.split('\n')
    out = {'itemizations': {}}
    for sched in 'ABCDEF':
        out['itemizations']['Schedule ' + sched] = []
    for i in range(len(lines)):
        line = lines[i]
        parsed = parseline(line, version)
        if parsed and 'fec_version' in parsed:
            version = parsed['fec_version']
        if i < 2:
            for k in parsed.keys():
                out[k] = parsed[k]
        elif parsed:
            for sched in 'ABCDEF':
                if parsed['form_type'][1] == sched:
                    out['itemizations']['Schedule ' + sched].append(parsed)
    return out


def parseline(line, version):
    fields = line.split(chr(0x1c))
    for mapping in mappings.keys():
        if re.match(mapping, fields[0], re.IGNORECASE):
            versions = mappings[mapping].keys()
            for v in versions:
                ver = version if version else fields[2]
                if re.match(v, ver, re.IGNORECASE):
                    out = {}
                    for i in range(len(mappings[mapping][v])):
                        out[mappings[mapping][v][i]] = fields[i]
                    return out
    return None
