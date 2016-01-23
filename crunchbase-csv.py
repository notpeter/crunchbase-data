import argparse
import re
import unicodecsv
import openpyxl


def crunchbase_csv_export(filename):
    """Convert crunchbase_export.xlsx to individual CSVs"""

    print "Reading from Excel Workbook '%s' (please wait...)" % filename
    workbook = openpyxl.load_workbook(filename=filename)
    for sheet_name in ['Companies', 'Rounds', 'Investments', 'Acquisitions', 'Additions']:
        sheet = workbook[sheet_name]
        header = [k.value for k in sheet.rows[0]]
        # skip empty and reduced precision date columns
        ignore_columns = {None, 'quarter_str', 'year_str,'
                   'acquired_month', 'acquired_quarter', 'acquired_year',
                   'founded_month', 'founded_quarter', 'founded_year',
                   'funded_month', 'funded_quarter', 'funded_year'}
        lines = []
        for row in sheet.rows:
            clean_row = []
            for cell in row:
                # FIXME: Find better way to determine a cell's header
                if header[ord(cell.column) - ord('A')] in ignore_columns:
                    pass
                elif isinstance(cell.value, basestring) and re.match(r'^(1000|0[0-2]\d\d)-', cell.value):
                    print "Cell {0.coordinate} is probably an invalid date ({0.value})".format(cell)
                    clean_row.append(None)
                elif hasattr(cell.value, 'date'):
                    clean_row.append(cell.value.date())  # converts datetime to date
                else:
                    clean_row.append(cell.value)
            # We only care about non-empty rows
            if clean_row.count(None) != len(clean_row):
                lines.append(clean_row)

        with open('%s.csv' % sheet_name.lower(), 'wb') as f:
            csv_out = unicodecsv.writer(f, lineterminator='\n')
            csv_out.writerow(lines.pop(0))  # header
            for line in sorted(lines):
                csv_out.writerow(line)
            print "%s: %s rows processed." % (sheet_name.lower(), sheet.max_row)
    print "Done!"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert crunchbase_export.xlsx to CSV")
    parser.add_argument('filename', default='crunchbase_export.xlsx', nargs='?')
    args = parser.parse_args()
    crunchbase_csv_export(args.filename)
