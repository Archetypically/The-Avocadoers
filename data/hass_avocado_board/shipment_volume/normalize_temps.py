#!python3.6
"""
normalize_dates.py

Usage: python3 normalize_dates.py <list of .csv files>

Reports 

Outputs cleaned data to <same_file_name>.csv
"""
from datetime import datetime
import argparse
import csv
import logging
import sys
import time

LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
INTERESTED_KEYS = [
    "YEAR",
    "WEEK IN YEAR",
    "VOLUME",
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
        description="Reformat passed in .csv file(s) to standard Year:WeekInYear:Value columns."
    )
    parser.add_argument(
        "file", nargs="*", type=argparse.FileType("r", encoding='utf-8-sig'), help="The name(s) of a file to normalize."
    )
    parser.add_argument("-v", "--verbose", action="count", default=3)
    args = parser.parse_args()
    logger = set_up_logger(args.verbose)
    logger.debug(f"ARGS: {args}")
    for dirty_csv in args.file:
        this_file_start = time.time()
        logger.info(f"Working on {dirty_csv.name}.")
        clean_rows = []
        this_csv_reader = csv.DictReader(dirty_csv)
        for row in this_csv_reader:
            # Jan-04-2015
            this_row_date = row["Week"]
            this_datetime = datetime.strptime(this_row_date, '%b-%d-%Y')
            this_row_value = row["California"]
            clean_row = {
                "YEAR": this_datetime.strftime("%Y").strip(),
                "WEEK IN YEAR": this_datetime.strftime("%U").strip(),
                "VOLUME": this_row_value
            }
            clean_rows.append(clean_row)
        this_file_dur = time.time() - this_file_start
        logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")
        logger.debug(f"CLEAN ROWS: {clean_rows[:10]}")
        clean_file_name = dirty_csv.name.replace("base", "normalized")
        logger.info(f"Writing out to file named: {clean_file_name}!")
        with open(clean_file_name, "w", newline="") as cleanfile:
            this_writer = csv.DictWriter(cleanfile, fieldnames=INTERESTED_KEYS)
            this_writer.writeheader()
            for row in clean_rows:
                this_writer.writerow(row)
        logger.info("Done writing file.")
        logger.info(f"Done processing file {dirty_csv.name}!")


if __name__ == "__main__":
    main()
