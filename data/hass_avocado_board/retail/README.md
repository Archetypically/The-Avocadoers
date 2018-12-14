# retail

This directory holds various retail data and manipulation scripts.

## Scripts

## fix_csv.py

Author: Evan Lee (@Archetypically)

*Requires python >=3.6*

Fixes column mis-alignment in raw HAB .csv files and throws away unnecessary data columns.

#### Usage

```bash
$ python3.6 fix_csv.py -h
usage: fix_csv.py [-h] [-v] [file [file ...]]

positional arguments:
  file           The name(s) of a file to normalize.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
```

#### Output

```bash
$ python3.6 fix_csv.py base/*.csv
[INFO]  Working on base/HAB_retail_2010.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: fixed/HAB_retail_2010.csv!
[INFO]  Done writing file.
[INFO]  Done processing file base/HAB_retail_2010.csv!
[INFO]  Working on base/HAB_retail_2011.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: fixed/HAB_retail_2011.csv!
[INFO]  Done writing file.
[INFO]  Done processing file base/HAB_retail_2011.csv!
[INFO]  Working on base/HAB_retail_2012.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: fixed/HAB_retail_2012.csv!
[INFO]  Done writing file.
[INFO]  Done processing file base/HAB_retail_2012.csv!
[INFO]  Working on base/HAB_retail_2013.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: fixed/HAB_retail_2013.csv!
[INFO]  Done writing file.
[INFO]  Done processing file base/HAB_retail_2013.csv!
[INFO]  Working on base/HAB_retail_2014.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: fixed/HAB_retail_2014.csv!
[INFO]  Done writing file.
[INFO]  Done processing file base/HAB_retail_2014.csv!
[INFO]  Working on base/HAB_retail_2015.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: fixed/HAB_retail_2015.csv!
[INFO]  Done writing file.
[INFO]  Done processing file base/HAB_retail_2015.csv!
[INFO]  Working on base/HAB_retail_2016.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: fixed/HAB_retail_2016.csv!
[INFO]  Done writing file.
[INFO]  Done processing file base/HAB_retail_2016.csv!
[INFO]  Working on base/HAB_retail_2017.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: fixed/HAB_retail_2017.csv!
[INFO]  Done writing file.
[INFO]  Done processing file base/HAB_retail_2017.csv!
```

## normalize_dates.py

Author: Evan Lee (@Archetypically)

*Requires python >=3.6*

Standardizes column format to Year:WeekNumber:Value column format.

#### Usage

```bash
$ python3.6 normalize_dates.py -h
usage: normalize_dates.py [-h] [-v] [file [file ...]]

positional arguments:
  file           The name(s) of a file to normalize.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
```

#### Output

```bash
$ python3.6 normalize_dates.py fixed/*.csv
[INFO]  Working on fixed/HAB_retail_2010.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: normalized/HAB_retail_2010.csv!
[INFO]  Done writing file.
[INFO]  Done processing file fixed/HAB_retail_2010.csv!
[INFO]  Working on fixed/HAB_retail_2011.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: normalized/HAB_retail_2011.csv!
[INFO]  Done writing file.
[INFO]  Done processing file fixed/HAB_retail_2011.csv!
[INFO]  Working on fixed/HAB_retail_2012.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: normalized/HAB_retail_2012.csv!
[INFO]  Done writing file.
[INFO]  Done processing file fixed/HAB_retail_2012.csv!
[INFO]  Working on fixed/HAB_retail_2013.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: normalized/HAB_retail_2013.csv!
[INFO]  Done writing file.
[INFO]  Done processing file fixed/HAB_retail_2013.csv!
[INFO]  Working on fixed/HAB_retail_2014.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: normalized/HAB_retail_2014.csv!
[INFO]  Done writing file.
[INFO]  Done processing file fixed/HAB_retail_2014.csv!
[INFO]  Working on fixed/HAB_retail_2015.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: normalized/HAB_retail_2015.csv!
[INFO]  Done writing file.
[INFO]  Done processing file fixed/HAB_retail_2015.csv!
[INFO]  Working on fixed/HAB_retail_2016.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: normalized/HAB_retail_2016.csv!
[INFO]  Done writing file.
[INFO]  Done processing file fixed/HAB_retail_2016.csv!
[INFO]  Working on fixed/HAB_retail_2017.csv.
[INFO]  Processing this file took 0.00 seconds.
[INFO]  Writing out to file named: normalized/HAB_retail_2017.csv!
[INFO]  Done writing file.
[INFO]  Done processing file fixed/HAB_retail_2017.csv!
```

## Data

### base

This directory holds the base data, straight from the HAB website.

### fixed

This directory holds corrected .csv data, including lining up the appropriate columns and removing unncessary data.

### normalized

This directory holds normalized, formatted data in Year,WeekInYear,Value format.