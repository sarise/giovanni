# Giovanni Scrapper

How to use
1. Download the GADM database files from https://gadm.org/download_country_v3.html
2. Decide the regio type to use: Provinsi, Kabupaten, Kecamatan. Down
   Example: Kabupaten --> /home/sari/repositories/mine/giovani/gadm/gadm36_IDN_2.shp
3. (Optional) Run the download_bbox script to convert the shapefile (.shp) to .csv
   Verify whether the generated csv file is sensible
4. Get the curl command from the browser

`curl "https://giovanni.gsfc.nasa.gov/giovanni/daac-bin/service_manager.pl?session=57962516-769C-11EA-8822-AE00DA5F715B^&service=ArAvTs^&starttime=2015-01-01T00:00:00Z^&endtime=2016-12-31T23:59:59Z^&bbox=95.8767,4.1072,96.4945,4.7971^&data=MOD08_M3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean_Mean^&dataKeyword=AOD^&portal=GIOVANNI^&format=json" ^
  -H "Connection: keep-alive" ^
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36" ^
  -H "Accept: */*" ^
  -H "Sec-Fetch-Site: same-origin" ^
  -H "Sec-Fetch-Mode: cors" ^
  -H "Sec-Fetch-Dest: empty" ^
  -H "Referer: https://giovanni.gsfc.nasa.gov/giovanni/" ^
  -H "Accept-Language: en-US,en;q=0.9,id;q=0.8,nl;q=0.7,ms;q=0.6" ^
  -H "Cookie: _ga=GA1.4.291996916.1596603126; _ga=GA1.2.291996916.1596603126; urs_guid_ops=e1059f4f-0668-4dcf-b37a-eb5cbc7941b8; _gid=GA1.2.1494757858.1599339914; _gid=GA1.4.1494757858.1599339914; 104121311146819161532179517180=s^%^3An3ksVMiavHpZerGgN9Va4UHH_ACZ5R1G.WU1R5TAxdBCg6peeXoJXJcMhJ5njTeQyWQMeWBh^%^2Boq8; giovanniUid=pugosambodo; userSessions=^%^7B^%^22userSessions^%^22^%^3A^%^7B^%^22pugosambodo^%^22^%^3A^%^7B^%^22GIOVANNI^%^22^%^3A^%^7B^%^22session^%^22^%^3A^%^2257962516-769C-11EA-8822-AE00DA5F715B^%^22^%^7D^%^7D^%^7D^%^7D" ^
  --compressed`
