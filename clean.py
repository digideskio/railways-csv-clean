#!/usr/bin/env python

import csv
import sys

CSV_FILE='/Users/martijnv/tmp/crossings/gcispubl.csv'  # input csv file
CSV_OUTFILE='/Users/martijnv/tmp/crossings/gcispubl_clean.csv'  # output csv file
LON_FIELD_LOC=84  # position of longitude field (0 based)
LAT_FIELD_LOC=83  # position of latitude field (0 based)
OUT_LON_FIELDNAME = 'lon'  # desired name out output longitude field
OUT_LAT_FIELDNAME = 'lat'  # desired name out output latitude field
ROWS_TO_KEEP=[1, 3, 13]  # zero based positions of other salient fields you want to keep
DECIMAL_PRECISION=7  # decimal precision of lat / lon fields
DELIMITER_IN = ','  # delimiter used in input CSV file
DELIMITER_OUT = ','  # desired delimiter for output CSV file
SKIP_NULL_ISLAND = True  # filter out 0,0 coordinates (duh)

failed_rows = []
row_count = 0
out_rows = []

with open (CSV_FILE, 'rb') as csv_file:
    sys.stdout.write('reading')
    first = True
    csv_reader = csv.reader(csv_file, delimiter=DELIMITER_IN)
    for row in csv_reader:
        if first:
            first = False
            out_header_row = [row[n] for n in ROWS_TO_KEEP]
            out_header_row.extend([OUT_LON_FIELDNAME, OUT_LAT_FIELDNAME])
            out_rows.append(out_header_row)
            continue
        lon = row[LON_FIELD_LOC]
        lat = row[LAT_FIELD_LOC]
        try:
            lat = float('{}.{}'.format(
                lat[:len(lat)-DECIMAL_PRECISION],
                lat[-DECIMAL_PRECISION:]))
            lon = float('{}.{}'.format(
                lon[:len(lon)-DECIMAL_PRECISION],
                lon[-DECIMAL_PRECISION:]))
            if SKIP_NULL_ISLAND:
                if lon == 0.0 or lat == 0.0:
                    continue
            out_row = [row[n] for n in ROWS_TO_KEEP]
            out_row.extend([lon, lat])
            out_rows.append(out_row)
        except ValueError, e:
            failed_rows.append(row)
        finally:
            row_count = row_count + 1
        if not row_count % 10e+3:
            sys.stdout.write('.')
            sys.stdout.flush()

with open (CSV_OUTFILE, 'wb') as csv_file:
    print '\nwriting'
    csv_writer = csv.writer(
        csv_file,
        delimiter=DELIMITER_OUT,
        quoting=csv.QUOTE_MINIMAL)
    for row in out_rows:
        csv_writer.writerow(row)

print 'out of {} rows in the input file, {} rows failed.'.format(row_count, len(failed_rows))
print 'done'