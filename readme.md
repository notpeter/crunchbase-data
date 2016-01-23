
# Crunchbase Data As CSV

This data was extracted from the December 4, 2015 [Crunchbase Data Export](http://info.crunchbase.com/about/crunchbase-data-exports/).

This repository includes unofficial CSV exports derived from the individual worksheets
from crunchbase_export.xlsx. I previously munged the data by hand with Excel,
but have since moved the dirty work to python.  Reading the XLSX file is
handled with [openpyxl](https://openpyxl.readthedocs.org/) while [unicodecsv](https://github.com/jdunck/python-unicodecsv) creates the CSVs.

The Excel workbook is transformed as follows:

 * One CSV file per worksheet
 * Skip the analysis page and empty columns
 * Remove redundant reduced precision date columns (month, quarter, year)
 * Remove dates missing a year (year 1000 is just wrong)
 * Remove trailing blank rows

## Usage

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python crunchbase-csv.py crunchbase_export.xlsx

## License

Use of this data is governed by the [CrunchBase Terms of Service and Licensing Policy](http://info.crunchbase.com/docs/terms-of-service/).

This data dump for non-commercial use is provided under
[Creative Commons Attribution-NonCommercial (CC-BY-NC)](http://creativecommons.org/licenses/by-nc/4.0/) license. Any commercial use requires a seperate license from CrunchBase.

crunchbase-csv.py is Copyright (c) Peter Tripp and made available under terms of the [MIT License](https://opensource.org/licenses/MIT)
