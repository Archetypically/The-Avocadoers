#!python3.6
"""
Usage: python3 fix_csv.py <list of .csv files>

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
    "PRICE",
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
        description="Fixes broken .csv files from the Hass Avocado Board."
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
        for row in dirty_csv:
            row_parts = row.split(",")
            clean_row = f"{row_parts[0]},{row_parts[-1]}"
            clean_rows.append(clean_row)
        this_file_dur = time.time() - this_file_start
        logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")
        logger.debug(f"CLEAN ROWS: {clean_rows[:10]}")
        clean_file_name = dirty_csv.name.replace("base", "fixed")
        logger.info(f"Writing out to file named: {clean_file_name}!")
        with open(clean_file_name, "w", newline="") as cleanfile:
            for row in clean_rows:
                cleanfile.write(row)
        logger.info("Done writing file.")
        logger.info(f"Done processing file {dirty_csv.name}!")


if __name__ == "__main__":
    main()
