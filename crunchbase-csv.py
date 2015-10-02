import argparse
import unicodecsv
import openpyxl

def crunchbase_csv_export(filename):
    """Convert crunchbase_export.xlsx to individual CSVs"""

    print "Reading from Excel Workbook '%s' (please wait...)" % filename
    try:
        workbook = openpyxl.load_workbook(filename=filename)
    # Quiets the (likely) harmless warning openpyxl emits:
    # UserWarning: Discarded range with reserved name
    except UserWarning:
        pass

    for sheet_name in ['Companies', 'Rounds', 'Investments', 'Acquisitions', 'Additions']:
        sheet = workbook[sheet_name]
        header = [k.value for k in sheet.rows[0]]
        # skip empty and reduced precision date columns
        ignore_columns = [None, 'quarter_str', 'year_str,'
            'acquired_month', 'acquired_quarter', 'acquired_year',
            'founded_month', 'founded_quarter', 'founded_year',
            'funded_month', 'funded_quarter', 'funded_year']
        with open('%s.csv' % sheet_name, 'wb') as f:
            csv_out = unicodecsv.writer(f)
            for row in sheet.rows:
                values = []
                for cell in row:
                    # There must be a simpler way to get the column header for a cell
                    if header[ord(cell.column)-65] not in ignore_columns:
                        if isinstance(cell.value, basestring) and cell.value.startswith('1000-'):
                            print "%s: Likely invalid date: %s" % (cell.coordinate, cell.value)
                            val = None
                        elif hasattr(cell.value, 'date'):
                            val = cell.value.date() # converts datetime to date
                        else:
                            val = cell.value
                        values.append(val)
                csv_out.writerow(values)
        print "%s.csv: %s rows processed." % (sheet_name, sheet.max_row)
    print "Done!"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert crunchbase_export.xlsx to CSV")
    parser.add_argument('filename', default='crunchbase_export.xlsx', nargs='?')
    args = parser.parse_args()
    crunchbase_csv_export(args.filename)
