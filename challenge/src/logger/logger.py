#!/usr/bin/env python3

import csv
import typing


class Logger:
    """ Simple CSV file writer for the simulation results."""

    csvfile: typing.TextIO
    writer: csv.writer

    def __init__(self, filepath):
        self.csvfile = open(filepath, 'w', newline='')
        self.writer = csv.writer(self.csvfile, delimiter=',')

    def writerow(self, row):
        self.writer.writerow(row)

    def close(self):
        self.csvfile.close()


if __name__ == '__main__':
    logger = Logger()
    logger.writerow(['Datetime', 'Pac_HH[kW]', 'Pac_PV[kW]', 'Pac_sum[kW]'])
    logger.close()
