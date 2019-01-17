import re


MAPPING_CACHE_KEY = "%s:%s"
MAPPING_CACHE = {}

TYPE_CACHE_KEY = "%s:%s:%s"
TYPE_CACHE = {}


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


def getMapping_from_regex(mappings, form, version):
    """ Raises FecParserMissingMappingError if missing"""

    for mapping in mappings.keys():
        if re.match(mapping, form, re.IGNORECASE):
            versions = mappings[mapping].keys()
            for v in versions:
                if re.match(v, version, re.IGNORECASE):
                    return(mappings[mapping][v])

    raise FecParserMissingMappingError({
        'form': form,
        'version': version,
    })


def getMapping(mappings, form, version):
    """ Tries to find the mapping from cache before looking it up w regex """
    key = MAPPING_CACHE_KEY % (form, version)
    try:
        mapping = MAPPING_CACHE[key]
    except KeyError:
        mapping = getMapping_from_regex(mappings, form, version)
        MAPPING_CACHE[key] = mapping
    return mapping


def getTypeMapping_from_regex(types, form, version, field):
    """ Tries to find the mapping from cache before looking it up w regex """
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
                            return prop
    return None


def getTypeMapping(types, form, version, field):
    """ caches the mapping to dict """
    key = TYPE_CACHE_KEY % (form, version, field)
    try:
        mapping = TYPE_CACHE[key]
    except KeyError:
        mapping = getTypeMapping_from_regex(types, form, version, field)
        TYPE_CACHE[key] = mapping
    return mapping
