__author__ = 'Yijun Pan'

import csv

class csvWriter:
    __dataset = None

    def __init__(self, dataset=None):
        self.__dataset = dataset

    def write_to_file(self, output_file="output.csv", delimiter=','):
        if not self.__dataset:
            print "Empty dataset. Nothing is written to file."

        with open(output_file, 'wb') as fp:
            fieldnames = self.__dataset[0].__dict__.keys()
            writer = csv.DictWriter(fp, fieldnames=fieldnames, delimiter=delimiter)

            # Write the first row with names of attributes
            writer.writeheader()

            # Write values line by line
            for data in self.__dataset:
                writer.writerow(data.__dict__.values())
