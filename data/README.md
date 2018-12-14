# data

This directory holds all data in sub-directories and raw final results.

## Scripts

## combine_all.py

Author: Evan Lee (@Archetypically)

*Requires python >=3.6*

#### Usage

```bash
$ python3.6 combine_all.py --climate-data=climate/california_total_scored.csv --shipment-data hass_avocado_board/shipment_volume/normalized/*.csv --retail-data hass_avocado_board/retail/normalized/*.csv
```

```bash
$ python3.6 combine_all.py -h
usage: combine_all.py [-h] --climate-data CLIMATE_DATA_FILE --shipment-data
                      [SHIPMENT_DATA_FILES [SHIPMENT_DATA_FILES ...]]
                      --retail-data
                      [RETAIL_DATA_FILES [RETAIL_DATA_FILES ...]] [-v]

Combine all datasets and report results.

optional arguments:
  -h, --help            show this help message and exit
  --climate-data CLIMATE_DATA_FILE
                        The name of normalized, aggregated, and scored climate
                        data.
  --shipment-data [SHIPMENT_DATA_FILES [SHIPMENT_DATA_FILES ...]]
                        The name(s) of normalized shipment data.
  --retail-data [RETAIL_DATA_FILES [RETAIL_DATA_FILES ...]]
                        The name(s) of normalized retail data.
  -v, --verbose
```

