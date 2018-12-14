#!python3.6
"""
combine_all.py

Usage: python3 combine_all.py --climate-data=<list of .csv files> --shipment-data=<list of .csv files> --retail-data=<list of .csv files> 

Outputs results to final_results.csv
"""
from datetime import datetime
import argparse
import csv
import logging
import json
import statistics
import sys
import time

LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
INTERESTED_KEYS = [
    "YEAR",
    "WEEK_IN_YEAR",
    "PRICE",
    "EFFECTIVE_VOLUME",
    "AVERAGE_WEIGHT",
    "WEIGHTS_IMPACTING"
]

def set_up_logger(verbose):
    try:
        log_level = LOG_LEVELS.pop(verbose)
    except IndexError:
        log_level = logging.DEBUG
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter("[%(levelname)s]\t%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger


def main():
    parser = argparse.ArgumentParser(
        description="Combine all datasets and report results."
    )
    parser.add_argument(
        "--climate-data", dest="climate_data_file", nargs=1, required=True, type=argparse.FileType("r", encoding='utf-8-sig'), help="The name of normalized, aggregated, and scored climate data."
    )
    parser.add_argument(
        "--shipment-data", dest="shipment_data_files", nargs="*", required=True, type=argparse.FileType("r", encoding='utf-8-sig'), help="The name(s) of normalized shipment data."
    )
    parser.add_argument(
        "--retail-data", dest="retail_data_files", nargs="*", required=True, type=argparse.FileType("r", encoding='utf-8-sig'), help="The name(s) of normalized retail data."
    )
    parser.add_argument("-v", "--verbose", action="count", default=3)
    args = parser.parse_args()
    logger = set_up_logger(args.verbose)
    logger.debug(f"ARGS: {args}")

    logger.info("Processing retail data...")
    timestamp_mappings = {}
    for this_csv in args.retail_data_files:
        this_file_start = time.time()
        logger.info(f"Working on {this_csv.name}.")
        clean_rows = []
        this_csv_reader = csv.DictReader(this_csv)
        for row in this_csv_reader:
            this_year = row["YEAR"]
            this_week = row["WEEK IN YEAR"]
            this_price = row["PRICE"]
            if this_year not in timestamp_mappings:
                timestamp_mappings[this_year] = {}
            if this_week not in timestamp_mappings[this_year]:
                timestamp_mappings[this_year][this_week] = {}

            timestamp_mappings[this_year][this_week]["PRICE"] = this_price
        this_file_dur = time.time() - this_file_start
        logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")

    logger.debug(f"{json.dumps(timestamp_mappings)}")

    logger.info("Processing shipment data...")
    all_shipment_data = {}
    for this_csv in args.shipment_data_files:
        this_file_start = time.time()
        logger.info(f"Working on {this_csv.name}.")
        clean_rows = []
        this_csv_reader = csv.DictReader(this_csv)
        for row in this_csv_reader:
            this_year = row["YEAR"]
            this_week = int(row["WEEK IN YEAR"]) - 1
            this_volume = row["VOLUME"]
            if this_year not in all_shipment_data:
                all_shipment_data[this_year] = []
            all_shipment_data[this_year].insert(this_week, this_volume)
        this_file_dur = time.time() - this_file_start
        logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")
    logger.debug(f"SHIPMENT DATA: {json.dumps(all_shipment_data)}")

    logger.info("Processing climate data...")
    all_climate_data = {}
    this_csv = args.climate_data_file[0]
    this_file_start = time.time()
    logger.info(f"Working on {this_csv.name}.")
    clean_rows = []
    this_csv_reader = csv.DictReader(this_csv)
    for row in this_csv_reader:
        this_year = row["YEAR"]
        this_week = int(row["WEEK OF YEAR"])
        this_score = int(row["SCORE"])
        if this_year not in all_climate_data:
            all_climate_data[this_year] = []
        all_climate_data[this_year].insert(this_week, this_score)
    this_file_dur = time.time() - this_file_start
    logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")
    logger.debug(f"CLIMATE DATA: {json.dumps(all_climate_data)}")

    output_rows = []
    num_weeks_required = 104
    for year, weeks in timestamp_mappings.items():
        for week_number, week_container in weeks.items():

            this_week_num = int(week_number)
            interested_year = all_shipment_data[year]
            try:
                interested_week = this_week_num - 2
                if interested_week < 0:
                    raise IndexError
                effective_volume = interested_year[interested_week]
            except IndexError:
                interested_year = str(int(year) - 1)
                try:
                    interested_year = all_shipment_data[interested_year]
                except KeyError:
                    continue
                effective_volume = interested_year[this_week_num-2]
            week_container["EFFECTIVE_VOLUME"] = effective_volume

            this_year_weeks_required = this_week_num - 2
            previous_years_weeks_required = num_weeks_required - this_year_weeks_required
            previous_two_years_weeks_required = previous_years_weeks_required - 52
            this_week_weights = []
            if this_year_weeks_required >= 0:
                this_week_weights += all_climate_data[year][:this_year_weeks_required]
            previous_year = str(int(year) - 1)
            this_week_weights += all_climate_data[previous_year]
            previous_previous_year = str(int(year) - 2)
            this_week_weights += all_climate_data[previous_year][len(all_climate_data[previous_year]) - previous_two_years_weeks_required:]

            week_container["WEIGHTS_IMPACTING"] = this_week_weights
            week_container["AVERAGE_WEIGHT"] = statistics.mean(this_week_weights)

            this_week_container = {
                "YEAR": year,
                "WEEK_IN_YEAR": this_week_num,
                "PRICE": week_container["PRICE"],
                "EFFECTIVE_VOLUME": week_container["EFFECTIVE_VOLUME"],
                "AVERAGE_WEIGHT": week_container["AVERAGE_WEIGHT"],
                "WEIGHTS_IMPACTING": week_container["WEIGHTS_IMPACTING"],
            }
            output_rows.append(this_week_container)

    logger.debug(f"{json.dumps(timestamp_mappings)}")
    clean_file_name = "final_results.csv"
    logger.info(f"Writing out to file named: {clean_file_name}!")
    with open(clean_file_name, "w", newline="") as cleanfile:
        this_writer = csv.DictWriter(cleanfile, fieldnames=INTERESTED_KEYS)
        this_writer.writeheader()
        for row in output_rows:
            this_writer.writerow(row)
    logger.info("Done writing file.")


if __name__ == "__main__":
    main()
