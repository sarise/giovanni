import csv

import shapefile
from glob import glob


def main():
    files = glob('/home/sari/repositories/mine/giovani/gadm/*.shp')
    for filename in files:
        sf = shapefile.Reader(filename)
        output_file = filename.replace('.shp', '.csv')
        print(output_file)
        with open(output_file, 'wb') as csvfile:
            keys = sorted(sf.record().as_dict().keys())
            if output_file.endswith('gadm36_IDN_2.csv'):
                keys = ['NAME_0', 'NAME_1', 'NAME_2', 'TYPE_2', 'CC_2']
            headers = keys + ['bbox']

            out_csv = csv.DictWriter(csvfile, headers, extrasaction='ignore')
            out_csv.writeheader()
            for item in sf.shapeRecords():
                row = item.record.as_dict()
                row['bbox'] = ', '.join(map(lambda x: '%0.4f' % x, item.shape.bbox))
                out_csv.writerow(row)
        sf.close()


if __name__ == '__main__':
    main()