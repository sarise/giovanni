import csv
import os
from glob import glob

OUTPUT_DIR = '/home/sari/repositories/mine/giovani/output/'
SATELLITES = ('OMAERUVd_003', 'OMTO3d_003')
SATELLITES = (
    'MYD08_D3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean',
    'MYD08_D3_6_1_Aerosol_Optical_Depth_Land_Ocean_Mean',
    'MYD08_D3_6_1_AOD_550_Dark_Target_Deep_Blue_Combined_Mean',
)
SATELLITES = (
    'MYD08_M3_6_1_Aerosol_Optical_Depth_Land_Ocean_Mean_Mean',
    'MYD08_M3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean_Mean',
)

SATELLITES = (
    'MOD08_M3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean_Mean',
)


def get_filename(satelit, kabupaten_id):
    filename_star = os.path.join(
        OUTPUT_DIR,
        'g4.areaAvgTimeSeries.%s.*_%s.csv' % (satelit, str(kabupaten_id)),
    )

    possible_files = glob(filename_star)
    assert len(possible_files) == 1
    return possible_files[0]


def read_data_file(kabupaten_name, kabupaten_id):
    # TODO: don't repeat things lah
    satellite1 = SATELLITES[0]
    filename1 = get_filename(satellite1, kabupaten_id)

    with open(filename1) as csv_file1:
        csv_reader1 = list(csv.reader(csv_file1, delimiter=','))
        start_reading = False
        result = []
        for i in range(len(csv_reader1)):
            if start_reading:
                result.append(
                    [kabupaten_name, kabupaten_id]
                    + csv_reader1[i]
                )

            # To ignore the first new lines in the input data file
            start_reading = start_reading or ('time' in csv_reader1[i])
        return result


def get_kabupaten_ids():
    with open('/home/sari/repositories/mine/giovani/gadm/gadm36_IDN_2.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            yield row['NAME_2'], row['CC_2']


def get_downloaded_kabupaten_ids():
    existing_files = glob('/home/sari/repositories/mine/giovani/output/g4*.csv')
    return map(lambda x: x[-8:-4], existing_files)


def main():
    aggregate_file = os.path.join(OUTPUT_DIR, 'aggregate.csv')
    print(aggregate_file)

    downloaded_kabupaten_ids = get_downloaded_kabupaten_ids()
    skipped = []
    not_skipped = []
    with open(aggregate_file, 'wb') as csvfile:
        headers = ['NAME_2', 'CC_2', 'TIME', SATELLITES[0]]
        out_csv = csv.writer(csvfile)
        out_csv.writerow(headers)
        for kabupaten_name, kabupaten_id in get_kabupaten_ids():
            if kabupaten_id not in downloaded_kabupaten_ids:
                print kabupaten_id, 'skipped'
                skipped.append(kabupaten_id)
                continue
            not_skipped.append(kabupaten_id)
            data = read_data_file(kabupaten_name, kabupaten_id)
            out_csv.writerows(data)
    print('Skipped: ', len(skipped))
    print('Not skipped: ', len(not_skipped))
    print('OK')


if __name__ == '__main__':
    main()