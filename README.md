# fecfile
a python parser for the .fec file format

This is a library for converting campaign finance filings stored in the .fec format into native python objects. It maps the comma/ASCII 28 delimited fields to canonical names based on the version the filing uses and then converts the values that are dates and numbers into the appropriate `int`, `float`, or `datetime` objects.

This library is in relatively early testing. I've used it on a couple of projects, but I wouldn't trust it to work on all filings. That said, if you do try using it, I'd love to hear about it!

## Why?
The FEC makes a ton of data available via the "export" links on the main site and the [developer API](https://api.open.fec.gov/developers/). For cases where those data sources are sufficient, they are almost certainly the easiest/best way to go. A few cases where one might need to be digging into raw filings are:

- Getting information from individual itemizations including addresses
- Getting data as soon as it has been filed, instead of waiting for it to be coded. (The FEC generally codes all filings received by 7pm eastern by 7am the next day. However, that means that a filing received at 11:59pm on Monday wouldn't be available until 7am on Wednesday, for example.)
- Getting more data than the rate-limit on the developer API would allow
- Maintaining ones own database with all relevant campaign finance data, perhaps synced with another data source

Raw filings can be found by either downloading the [bulk data](https://www.fec.gov/data/advanced/?tab=bulk-data) zip files or from http requests like [this](http://docquery.fec.gov/dcdev/posted/1229017.fec). This library includes helper methods for both.

## Installation
To get started, install from [pypi](https://pypi.org/project/fecfile/) by running the following command in your preferred terminal:

```
pip install fecfile
```

## Usage
For the vast majority of filings, the easiest way to use this library will be to load filings all at once by using the `from_http(file_number)`, `from_file(file_path)`, or `loads(input)` methods.

These methods will return a Python dictionary, with keys for `header`, `filing`, `itemizations`, and `text`. The `itemizations` dictionary contains lists of itemizations grouped by type (`Schedule A`, `Schedule B`, etc.).

### Examples:

```
import fecfile

filing1 = fecfile.from_file('1229017.fec')
print('${:,.2f}'.format(filing1['filing']['col_a_total_receipts']))

filing2 = fecfile.from_http(1146148)
print(filing2['filing']['committee_name'])

filing3 = fecfile.from_http(1146148)
all_contributions = filing3['itemizations']['Schedule B']
mid_size_contributions = [item for item in all_contributions if 500 <= item[contribution_amount] < 1000]
print(len(mid_size_contributions))

with open('1229017.fec') as file:
    parsed = fecfile.loads(file.read())
    num_disbursements = len(parsed['itemizations']['Schedule B'])
    print(num_disbursements)

url = 'http://docquery.fec.gov/dcdev/posted/1229017.fec'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
parsed = fecfile.loads(r.text)
fecfile.print_example(parsed)
```

Note: the docquery.fec.gov urls cause problems with the requests library when a user-agent is not supplied. There may be a cleaner fix to that though.

## Advanced Usage

For some large filings, loading the entire filing into memory like the above examples do would not be a good idea. For those cases, the `fecfile` library provides the `iter_file` and `iter_http` methods. Both are generator functions that yield `FecItem` objects, which consist of `data` and `data_type` attributes. The data_type attribute can be one of "header", "summary", "itemization", "text", or "F99_text". The data attribute is a dictionary for all data types except for "F99_text", for which it is a string.

```
import fecfile
import imaginary_database

# sometimes we only care about summary data, but want to be able to handle all filings, without
# knowing anything about them before we attempt to parse.
no_itemizations = {'filter_itemizations': []}
for i in range(1300000, 1320000):
    for item in fecfile.iter_http(i, options=no_itemizations):
        if item.data_type == 'summary':
            imaginary_database.add_to_db(item.data)

# Sometimes we only care about one type of itemization, but from a very large filing.
# In this example, we add up all the contributions from Delaware in ActBlue's 2018
# post-general filing
only_contributions = {'filter_itemizations': ['SA']}
de_total = 0
for item in fecfile.iter_http(1300352, options=only_contributions):
    if item.data_type == 'itemization':
        if item.data['contributor_state'] == 'DE':
            de_total += item.data['contribution_amount']
print(de_total)

# Sometimes we want to maintain a database where different types of itemizations live in their own
# tables and have foreign key relationships to a summary record.
file_path = '/path/to/99840.fec'
filing = None
for item in fecfile.iter_file(file_path):
    if item.data_type == 'summary':
        filing = imaginary_database.add_filing(file_number=99840, **item.data)
    if item.data_type == 'itemization':
        if item.data['form_type'].startswith('SA'):
            imaginary_database.add_contribution(filing=filing, **item.data)
        if item.data['form_type'].startswith('SB'):
            imaginary_database.add_disbursement(filing=filing, **item.data)
        if item.data['form_type'].startswith('SC'):
            imaginary_database.add_loan(filing=filing, **item.data)
```

You can also choose to use the `parse_header` and `parse_line` methods if you are implementing a different method of
iterating over a filing's content. Before version 0.6, the below example was the only way to use `fecfile` to parse
filings without loading the entire filing into memory. This approach should no longer be necessary, but is kept to
show how example usage for those methods.

```
import fecfile

version = None

with open('1263179.fec') as file:
    for line in file:
        if version is None:
            header, version = fecfile.parse_header(line)
        else:
            parsed = fecfile.parse_line(line, version)
            save_to_db(parsed)
```


## API Reference

<h3 id="fecfile.loads">loads</h3>

```
loads(input, options={})
```
Deserialize ``input`` (a ``str`` instance
containing an FEC document) to a Python object.

Optionally, pass an array of strings to ``options['filter_itemizations']``.
If included, ``loads`` will only parse lines that start with any of the
strings in that array. For example, passing
``{'filter_itemizations': ['SC', 'SD']}`` to ``options``, will only include
Schedule C and Schedule D itemizations. Also, passing
``{'filter_itemizations': []}`` to ``options`` will result in only the header
and the filing being parsed and returned.

Including `{'as_strings': True}` in the `options` dictionary will not attempt to convert values that are normally numeric or datetimes to their native python types and will return dictionaries with all values as strings.

<h3 id="fecfile.parse_header">parse_header</h3>

```
parse_header(hdr)
```
Deserialize a ``str`` or a list of ``str`` instances containing
header information for an FEC document. Returns an Python object, the
version ``str`` used in the document, and the number of lines used
by the header.

The third return value of number of lines used by the header is only
useful for versions 1 and 2 of the FEC file format, when the header
was a multiline string beginning and ending with ``/*``. This allows
us to pass in the entire contents of the file as a list of lines and
know where to start parsing the non-header lines.

<h3 id="fecfile.parse_line">parse_line</h3>

```
parse_line(line, version, line_num=None)
```
Deserialize a ``line`` (a ``str`` instance
containing a line from an FEC document) to a Python object.

``version`` is a ``str`` instance for the version of the FEC file format
to be used, and is required.

``line_num`` is optional and is used for debugging. If an error or
warning is encountered, whatever is passed in to ``line_num`` will be
included in the error/warning message.

<h3 id="fecfile.from_http">from_http</h3>

```
from_http(file_number, options={})
```
Utility method for getting a parsed Python representation of an FEC
filing when you don't already have it on your computer. This method takes
either a ``str`` or ``int`` as a ``file_number`` and requests it from
the ``docquery.fec.gov`` server, then parses the response.

See [above](#fecfile.loads) for how documentation on how to use the optional
``options`` argument.

<h3 id="fecfile.from_file">from_file</h3>

```
from_file(file_path, options={})
```
Utility method for getting a parsed Python representation of an FEC
filing when you have the .fec file on your computer. This method takes
a ``str`` of the path to the file, and returns the parsed Python object.

See [above](#fecfile.loads) for how documentation on how to use the optional
``options`` argument.

<h3 id="fecfile.iter_http">iter_http</h3>

```
iter_http(file_number, options={})
```
Makes an http request for the given `file_number` and iterates over the response, yielding `FecItem` instances, which consist of `data` and `data_type` attributes. The `data_type` attribute can be one of "header", "summary", "itemization", "text", or "F99_text". The `data` attribute is a dictionary for all data types except for "F99_text", for which it is a string. This method avoids loading the entire filing into memory, as the `from_http` method does.

See [above](#fecfile.loads) for how documentation on how to use the optional
``options`` argument.

<h3 id="fecfile.iter_file">iter_file</h3>

```
iter_file(file_path, options={})
```
Opens a file at the given `file_path` and iterates over its contents, yielding `FecItem` instances, which consist of `data` and `data_type` attributes. The `data_type` attribute can be one of "header", "summary", "itemization", "text", or "F99_text". The `data` attribute is a dictionary for all data types except for "F99_text", for which it is a string. This method avoids loading the entire filing into memory, as the `from_file` method does.

See [above](#fecfile.loads) for how documentation on how to use the optional
``options`` argument.

<h3 id="fecfile.print_example">print_example</h3>

```
print_example(parsed)
```
Utility method for debugging - prints out a representative subset of
the Python object returned by one of the deserialization methods. For
filings with itemizations, it only prints the first of each type of
itemization included in the object.


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

Many thanks to [Jacob Fenton](https://github.com/jsfenfen) for writing the caching logic and for providing valuable feedback about the overall design of this library.

## Contributing

I would love some help with this, particularly with the mapping from strings to `int`, `float`, and `datetime` types. Please [create an issue](https://github.com/esonderegger/fecfile/issues) or [make a pull request](https://github.com/esonderegger/fecfile/pulls). Or reach out privately via email - that works too.

## To do:

Almost too much to list:

- ~~Handle files from before v6 when they were comma-delimited~~
- create a `dumps` method for writing .fec files for round-trip tests
- add more types to the types.json file
- elegantly handle errors

## Changes

See the [changelog](https://esonderegger.github.io/fecfile/changelog.html) for a list of notable changes introduced in each version of fecfile.