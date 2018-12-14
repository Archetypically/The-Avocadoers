#!python3.6
"""
assign_weights.py

Usage: python3 assign_weights.py <list of .csv files>

Assigns weights to weeks based on the mean temperature for that day.

Outputs cleaned data to california_total_aggregated.csv
"""
from datetime import datetime
import argparse
import collections
import csv
import logging
import statistics
import sys
import time

LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
INTERESTED_KEYS = [
    "YEAR",
    "WEEK OF YEAR",
    "MEAN",
    "SCORE"
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
        description="Calculate and report weekly scores for the passed-in .csv file(s)."
    )
    parser.add_argument(
        "file", type=argparse.FileType("r"), help="The name of a file to assign weights to."
    )
    parser.add_argument("-v", "--verbose", action="count", default=5)
    args = parser.parse_args()
    logger = set_up_logger(args.verbose)
    logger.debug(f"ARGS: {args}")

    this_file_start = time.time()
    logger.info(f"Working on {args.file.name}.")
    this_csv_reader = csv.DictReader(args.file)

    clean_rows = []
    for row in this_csv_reader:
        clean_row = {
            "YEAR": row["YEAR"],
            "WEEK OF YEAR": row["WEEK OF YEAR"],
            "MEAN": row["MEAN"],
            "SCORE": round(abs(75.0 - float(row["MEAN"]))/3.0),
        }
        clean_rows.append(clean_row)
        
    this_file_dur = time.time() - this_file_start
    logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")

    clean_file_name = "california_total_scored.csv"
    logger.info(f"Writing out to file named: {clean_file_name}!")
    with open(clean_file_name, "w", newline="") as cleanfile:
        this_writer = csv.DictWriter(cleanfile, fieldnames=INTERESTED_KEYS) 
        this_writer.writeheader()
        for row in clean_rows:
            this_writer.writerow(row)
    logger.info("Done writing file.")

if __name__ == "__main__":
    main()
