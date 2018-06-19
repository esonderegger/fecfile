# fecfile
Python parser for the .fec file format

This is still in very early testing. The goal of this project is to take in a string in .fec format, either from the [bulk data](https://www.fec.gov/data/advanced/?tab=bulk-data) zip files or from an http request like [this](http://docquery.fec.gov/dcdev/posted/1229017.fec) and output a python dictionary, with native types for the number and date/time fields.

To use this locally, do something like:

```
import fecfile
import json

with open('1229017.fec') as file:
    parsed = fecfile.parse(file.read())
    print(json.dumps(parsed, sort_keys=True, indent=2))
```
