import csv
import os
import time
from glob import glob
from multiprocessing import Process, Pool

import requests
import uncurl
from urlparse import (
    parse_qsl,
    urlparse,
    urlsplit,
    urljoin,
)

HOME_PAGE = 'https://giovanni.gsfc.nasa.gov/giovanni/'
OUTPUT_DIR = '/home/sari/repositories/mine/giovani/output/'
SLEEP_SECONDS = 20

# Remove any special character like (^) when copy pasting from browser.
GENERATION_CURL= \
'''
curl "https://giovanni.gsfc.nasa.gov/giovanni/daac-bin/service_manager.pl?session=57962516-769C-11EA-8822-AE00DA5F715B&service=ArAvTs&starttime=2015-01-01T00:00:00Z&endtime=2016-12-31T23:59:59Z&bbox=95.8767,4.1072,96.4945,4.7971&data=MOD08_M3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean_Mean&dataKeyword=AOD&portal=GIOVANNI&format=json"
  -H "Connection: keep-alive" 
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36" 
  -H "Accept: */*" 
  -H "Sec-Fetch-Site: same-origin" 
  -H "Sec-Fetch-Mode: cors"
  -H "Sec-Fetch-Dest: empty"
  -H "Referer: https://giovanni.gsfc.nasa.gov/giovanni/"
  -H "Accept-Language: en-US,en;q=0.9,id;q=0.8,nl;q=0.7,ms;q=0.6"
  -H "Cookie: _ga=GA1.4.291996916.1596603126; _ga=GA1.2.291996916.1596603126; urs_guid_ops=e1059f4f-0668-4dcf-b37a-eb5cbc7941b8; _gid=GA1.2.1494757858.1599339914; _gid=GA1.4.1494757858.1599339914; 104121311146819161532179517180=s%3An3ksVMiavHpZerGgN9Va4UHH_ACZ5R1G.WU1R5TAxdBCg6peeXoJXJcMhJ5njTeQyWQMeWBh%2Boq8; giovanniUid=pugosambodo; userSessions=%7B%22userSessions%22%3A%7B%22pugosambodo%22%3A%7B%22GIOVANNI%22%3A%7B%22session%22%3A%2257962516-769C-11EA-8822-AE00DA5F715B%22%7D%7D%7D%7D"
  --compressed
'''
URL = 'https://giovanni.gsfc.nasa.gov/giovanni/daac-bin/service_manager.pl'

DOWNLOAD_CURL = \
'''
curl 'https://giovanni.gsfc.nasa.gov/giovanni/daac-bin/serializer.pl?SESSION=57962516-769C-11EA-8822-AE00DA5F715B&RESULTSET=F86CC828-F004-11EA-A940-ADEC5E835E51&RESULT=F86D782C-F004-11EA-A940-ADEC5E835E51&FILE=g4.areaAvgTimeSeries.MOD08_M3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean_Mean.20150101-20161231.95E_4N_96E_4N.nc'
 -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
 -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
 -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive'
 -H 'Cookie: _ga=GA1.2.1085750828.1585670900; _ga=GA1.4.1085750828.1585670900; urs_guid_ops=e1059f4f-0668-4dcf-b37a-eb5cbc7941b8; userSessions=%7B%22userSessions%22%3A%7B%22pugosambodo%22%3A%7B%22GIOVANNI%22%3A%7B%22session%22%3A%2257962516-769C-11EA-8822-AE00DA5F715B%22%7D%7D%7D%7D; nasa_gesdisc_data_archive=eTXMwfbDQPGp5PolAe9rKSdeOcMuHjz782KrlhFxpkO7et3hLJKYEGInAsJt7E/zUxni1LnpWsxHBZ1O4jFOdNLFQvCz7RBVzUVoEk/O7rKBps61s9U8hrt1Ff/R3GK4huvzly9ltJ2pzqB8FQ6VGA==; 104121311146819161532179517180=s%3AKKPPYmH6_x3Woncra0TrxX8NtPY4yJds.6U8LgPlfLKJ2hMwEoA9RhTWrl8hlZuu2svt8ItC%2FYbA; _gid=GA1.2.839318566.1599373418; _gid=GA1.4.839318566.1599373418; giovanniUid=pugosambodo'
 -H 'Upgrade-Insecure-Requests: 1'
'''

def curl_to_url_params_headers_cookies(curl_string):
    context = uncurl.parse_context(curl_string)
    url = urljoin(context.url, urlparse(context.url).path)
    params = parse_qsl(urlsplit(context.url).query)
    return url, params, context.headers, context.cookies


def download_file(place_id, download_url, filename):
    # curl3 = "curl 'https://giovanni.gsfc.nasa.gov/giovanni/daac-bin/serializer.pl?SESSION=57962516-769C-11EA-8822-AE00DA5F715B&RESULTSET=6E34DAD8-769C-11EA-B891-5D01DA5F715B&RESULT=6E3576D2-769C-11EA-B891-5D01DA5F715B&FILE=g4.areaAvgTimeSeries.MYD08_M3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean_Mean.20150101-20161231.92E_10S_140E_6N.nc' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://giovanni.gsfc.nasa.gov/giovanni/' -H 'Connection: keep-alive' -H 'Cookie: _ga=GA1.2.1085750828.1585670900; _ga=GA1.4.1085750828.1585670900; urs_guid_ops=e1059f4f-0668-4dcf-b37a-eb5cbc7941b8; userSessions=%7B%22userSessions%22%3A%7B%22pugosambodo%22%3A%7B%22GIOVANNI%22%3A%7B%22session%22%3A%2257962516-769C-11EA-8822-AE00DA5F715B%22%7D%7D%7D%7D; _gid=GA1.4.421050299.1586022345; _gid=GA1.2.421050299.1586022345; giovanniUid=pugosambodo; _gat_UA-112998278-65=1; nasa_gesdisc_data_archive=eTXMwfbDQPGp5PolAe9rKSdeOcMuHjz782KrlhFxpkO7et3hLJKYEGInAsJt7E/zUxni1LnpWsxHBZ1O4jFOdNLFQvCz7RBVzUVoEk/O7rKBps61s9U8hrt1Ff/R3GK4huvzly9ltJ2pzqB8FQ6VGA==' -H 'Upgrade-Insecure-Requests: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'"
    _, _, headers, cookies = curl_to_url_params_headers_cookies(DOWNLOAD_CURL)

    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)

    r = session.get(HOME_PAGE + download_url, allow_redirects=True)
    if len(r.content) < 100:
        print 'failed', r.url, '\n', r.content
        return

    filename = filename[:filename.find('.2014')] + '_' + place_id + '.csv'
    with open(os.path.join(OUTPUT_DIR, filename), 'wb') as f:
        f.write(r.content)


def process(file_id, bbox):
    file_id = str(file_id)
    url, old_params, headers, cookies = curl_to_url_params_headers_cookies(GENERATION_CURL)

    # Override the bbox param in the curl your own bbox
    params_to_update = [
        ('bbox', bbox),
        ('data', 'MOD08_M3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean_Mean'),
        ('dataKeyword', 'AOD'),
    ]

    dict_tmp = dict(old_params)
    dict_tmp.update(dict(params_to_update))
    params = list(dict_tmp.items())

    s = requests.Session()
    s.headers.update(headers)
    s.cookies.update(cookies)

    response = s.get(url, params=params)
    data = response.json()
    print file_id, ' 1 ', response.url

    progress = data['session']['resultset'][0]['result'][0]['status'][0]['percentComplete'][0]['value']
    while progress != '100':
        time.sleep(SLEEP_SECONDS)
        params = [
            ('session',     data['session']['id']),
            ('resultset',   data['session']['resultset'][0]['id']),
            ('result',      data['session']['resultset'][0]['result'][0]['id']),
            ('portal',      'GIOVANNI'),
            ('format',      'json'),
        ]
        response = s.get(URL, params=params)
        data = response.json()
        progress = data['session']['resultset'][0]['result'][0]['status'][0]['percentComplete'][0]['value']

        print file_id, ' 2 ', progress, response.url

    for item in data['session']['resultset'][0]['result'][0]['data'][0]['fileGroup']:
        result = item['dataFile'][0]['dataUrl'][1]
        download_url = result['value']
        filename = result['label']
        download_file(file_id, download_url, filename)


def get_downloaded_kabupaten_ids():
    existing_files = glob('/home/sari/repositories/mine/giovani/output/g4*.csv')
    return map(lambda x: x[-8:-4], existing_files)


def main():
    with open('/home/sari/repositories/mine/giovani/gadm/gadm36_IDN_2.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        count = 0
        for row in csv_reader:
            if str(row['CC_2']) in get_downloaded_kabupaten_ids():
                print row['CC_2'], 'done'
                continue

            process(row['CC_2'], row['bbox'])


if __name__ == '__main__':
    main()
