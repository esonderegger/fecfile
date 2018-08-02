# fecfile
a python parser for the .fec file format

This is still in very early testing. I wouldn't recommend relying on this library for anything important. That said, if you do try using it, I'd love to hear about it!

The goal of this project is to parse data in the .fec format and return a native python object. This is designed to work with either the [bulk data](https://www.fec.gov/data/advanced/?tab=bulk-data) zip files or from http requests like [this](http://docquery.fec.gov/dcdev/posted/1229017.fec) and includes helper methods for both.

## Installation
To get started, install from [pypi](https://pypi.org/project/fecfile/) by running the following command in your preferred terminal:

    pip install fecfile

## Usage (the hard way)
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

## Usage (the easy way)

```
import fecfile
import json

filing1 = fecfile.from_file('1229017.fec')
print(json.dumps(filing1, sort_keys=True, indent=2, default=str))

filing2 = fecfile.from_http(1146148)
print(json.dumps(filing2, sort_keys=True, indent=2, default=str))
```
Note the `default=str` parameter - that allows serializing to json dictionaries that contain datetime objects.

## Developing locally

Assuming you already have Python3 and the ability to create virtual environments installed, first clone this repository from github and cd into it:

```
git clone https://github.com/esonderegger/fecfile.git
cd fecfile
```

Then create a virtual environment for this project (I use the following commands, but there are several ways to get the desired result):

```
python3 -m venv ~/.virtualenvs/fecfile
source ~/.virtualenvs/fecfile/bin/activate
```

Next, install the dependencies:

```
python setup.py
```

Finally, make some changes, and run:

```
python tests.py
```

## Thanks

This project would be impossible without the work done by the kind folks at The New York Times [Newsdev team](https://github.com/newsdev). In particular, this project relies heavily on [fech](https://github.com/NYTimes/Fech) although it actually uses a transformation of [this fork](https://github.com/PublicI/fec-parse/blob/master/lib/renderedmaps.js).

## Contributing

I would love some help with this, particularly with the mapping from strings to `int`, `float`, and `datetime` types. Please [create an issue](https://github.com/esonderegger/fecfile/issues) or [make a pull request](https://github.com/esonderegger/fecfile/pulls). Or reach out privately via email - that works too.

## To do:

Almost too much to list:

- ~~Handle files from before v6 when they were comma-delimited~~
- create a `dumps` method for writing .fec files for round-trip tests
- add more types to the types.json file
- elegantly handle errors
