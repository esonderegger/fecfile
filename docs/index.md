---
layout: default
title: fecfile: a python parser for the .fec file format
---

# fecfile
a python parser for the .fec file format

This is still in very early testing. The goal of this project is to take in a string in .fec format, either from the [bulk data](https://www.fec.gov/data/advanced/?tab=bulk-data) zip files or from an http request like [this](http://docquery.fec.gov/dcdev/posted/1229017.fec) and output a python dictionary, with native types for the number and date/time fields.

To use this locally, do something like:

```
import fecfile
import json

with open('1229017.fec') as file:
    parsed = fecfile.loads(file.read())
    print(json.dumps(parsed, sort_keys=True, indent=2, default=str))
```

or:

```
import fecfile
import json
import requests

url = 'http://docquery.fec.gov/dcdev/posted/1229017.fec'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
parsed = fecfile.loads(r.text)
print(json.dumps(parsed, sort_keys=True, indent=2, default=str))
```

Note: the docquery.fec.gov urls cause problems with the requests library when a user-agent is not supplied. There may be a cleaner fix to that though.
