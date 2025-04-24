---
layout: default
title: A list of changes in each version of fecfile
---

# Changelog

A list of changes in each version of fecfile

### 0.9.0 (April 23, 2025)
- add support for version 8.5

### 0.8.0 (February 25, 2023)
- add some missing mappings from v5 of F3

### 0.7.2 (July 23, 2022)
- fix mappings for version 8.4 of F5

### 0.7.1 (July 16, 2022)
- fix mappings for version 8.4 of F3Z1 and F3Z2

### 0.7.0 (May 17, 2022)
- add support for version 8.4
- fix for version 2 of schedule A
- fix for `UnicodeDecodeError`

### 0.6.4 (September 3, 2020)
- add date types to schedule C
- include status code with error from `iter_http`

### 0.6.3 (June 3, 2019)
- use https for docquery.fec.gov URLs

### 0.6.2 (April 24, 2019)
- add mappings and types for F8, F82, and F83
- edits to documentation

### 0.6.1 (April 11, 2019)
- add mappings and types for F10 and F105
- add as_strings option to disable typing process
- raise exception when requests for a given file number do not succeed

### 0.6.0 (April 10, 2019)
- add iter_http and iter_file functions, using a shared iter_lines function
- refactor loads to use the new generator functions for performance

### 0.5.3 (February 12, 2019)
- handle trailing whitespace in form_type field
- fix regex for F1M
- fix F5 for P3.2 and P3.3

### 0.5.2 (January 19, 2019)
- add Form 1 mappings for version 2
- add Schedule F mappings for version 2
- update mappings regexes for F6 and F65
- add H4 mappings for version 2
- add H3 mappings for version 2

### 0.5.1 (January 18, 2019)
- update mappings versions for F3Z
- add mappings and types for schedule I
- allow filtering of itemizations for comma-delimited filings

### 0.5.0 (January 17, 2019)
- add ability to filter which types of itemizations to parse
- cache mappings and types for much faster parsing

### 0.4.11 (January 12, 2019)
- handle files encoded in Windows 1252
- fix for duplicate col_b_transfers_from_affiliated mapping
- allow for form F4T

### 0.4.10 (November 7, 2018)
- strip whitespace when parsing values as float or date
- fix mis-mapped field in paper F3 filings

### 0.4.9 (November 6, 2018)
- add mappings for paper versions of F24

### 0.4.8 (November 6, 2018)
- fix v5/3 mapping for F3P to include v1 and v2
- make F5 mappings more explicit and include v6.1
- add types for F3S

### 0.4.7 (November 2, 2018)
- add types for F4, SF, and SL
- fix issue causing incorrect mapping for F9

### 0.4.6 (October 29, 2018)
- add mappings for paper versions of F4
- add mappings for paper versions of F56
- add mappings for paper versions of F91
- add mappings for paper versions of F92
- add mappings for paper versions of F93
- add mappings for paper versions of F94
- add mappings for paper versions of F99
- add mappings for paper versions of H5 and H6
- add mappings for paper versions of Schedule L
- add mapping for version P3.4 for F3Z1 and F3Z2

### 0.4.5 (October 27, 2018)
- add mappings for paper versions of F3Z

### 0.4.4 (October 17, 2018)
- fixed out of order mappings for paper versions of F3

### 0.4.3 (October 10, 2018)
- add mappings for paper versions of F76
- add mappings for paper versions of F9
- add mappings for paper versions of F2
- add mappings for paper versions of F7

### 0.4.2 (October 9, 2018)
- add mappings for paper versions of F57
- add mappings for paper versions of F5
- add mappings for paper versions of F3L
- add mappings for paper versions of F3S

### 0.4.1 (October 4, 2018)
- add mappings for versions P1 and P2 of Schedule B
- add mappings for versions P1 and P2 of Schedule A
- add mappings for versions P1 and P2 of F3
- add F99_text field to returned object for form 99 filings
- add hdr mappings for paper versions 1 and 2
- do not split on commas when we know the form is using ascii 28
- add mappings for paper versions of F65
- add mappings for paper versions of schedule C1
- add mappings for paper versions of schedule C2
- add mappings for paper versions of schedule E

### 0.4.0 (October 2, 2018)
- Updated documentation
- add paper versions for schedule F

### 0.3.9 (October 1, 2018)
- add paper versions for H1, H2, H3, and H4

### 0.3.8 (September 28, 2018)
- add paper versions for the F1S

### 0.3.7 (September 27, 2018)
- add paper versions of F1M
- add paper versions for F3X
- add F3P paper filing mappings

### 0.3.6 (September 27, 2018)
- add F6 paper mappings and fix missing commas

### 0.3.5 (September 26)
- add all paper versions of form F1

### 0.3.4 (September 18, 2018)
- expose parse_header and parse_line to consumers of this library

### 0.3.3 (September 18, 2018)
- add version 8.3 to mappings

### 0.3.2 (August 29, 2018)
- versions 1 and 2 of schedule H1 and H2

### 0.3.1 (August 29, 2018)
- added more mappings
- add a method to determine which mappings are missing

### 0.3.0 (August 27, 2018)
- Rework warnings and errors for cases where mappings are missing
- add mappings

### 0.2.3 (August 24, 2018)
- fix for filings that use both quotes and the field separator

### 0.2.2 (August 23, 2018)
- add support for F13, F132, and F133

### 0.2.1 (August 21, 2018)
- Fix regression that broke paper filings

### 0.2.0 (August 2, 2018)
- Add parsing for versions 1 and 2 of the .fec format

### 0.1.9 (July 18, 2018)
- add parsing for senate paper filings

### 0.1.8 (June 26, 2018)
- interest rate should never have been a float field

### 0.1.7 (June 26, 2018)
- handle n/a in number fields

### 0.1.6 (June 25, 2018)
- more types
- update documentation
- handle percent signs in interest rates

### 0.1.5 (June 21, 2018)
- Initial published version
