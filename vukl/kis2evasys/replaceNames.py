#!/usr/bin/python3
'''
	sets correct values for full names and titles in EvaSys import file
'''

# This file is part of VUKL.
#
# VUKL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# VUKL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with VUKL.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Christian De Schryver"

import csv

# Verzeichnis für CSV-Dateien
DATA_DIRECTORY = "data/"

# generated output file from kis2evasys (may be modified first)
INPUT_FILENAME = DATA_DIRECTORY + "evasys-import-raw.csv"
# file encoding for input file
INPUT_FILE_ENCODING = "utf-8"

# target filename for updated names and titles
OUTPUT_FILENAME = DATA_DIRECTORY + "evasys-import-final.csv"
# desired file encoding for output file
OUTPUT_FILE_ENCODING = "latin-1"

# a fresh export of all users from EvaSys with required personal data
EXPORT_FILENAME = DATA_DIRECTORY + "evasys-export.csv"
# file encoding for EvaSys export file (default: latin-1)
EXPORT_FILE_ENCODING = "latin-1"

# determine required dialect for EvaSys import from EvaSys export file
with open(EXPORT_FILENAME, "r", encoding=EXPORT_FILE_ENCODING) as exportFile:
	dialect = csv.Sniffer().sniff(exportFile.read(1024))
# force quotes everywhere
dialect.quoting = csv.QUOTE_ALL
# set line endings to LF independent of OS default
dialect.lineterminator = "\n"

# determine dialect of input file
with open(INPUT_FILENAME, "r", encoding=INPUT_FILE_ENCODING) as inputFile:
	inputDialect = csv.Sniffer().sniff(inputFile.read(1024))

# add additional information for each person
with open(INPUT_FILENAME, "r", encoding=INPUT_FILE_ENCODING) as inputFile:
	inputReader = csv.reader(inputFile, inputDialect)
	with open(OUTPUT_FILENAME, "w", encoding=OUTPUT_FILE_ENCODING) as outputFile:
		outputWriter = csv.writer(outputFile, dialect)

		for row in inputReader:
			rowNew = row

			lastName = row[6]
			lastNameFound = False
			# search for last name in export file
			with open(EXPORT_FILENAME, "r", encoding=EXPORT_FILE_ENCODING) as exportFile:
				nameReader = csv.reader(exportFile, dialect)
				for nameRow in nameReader:
					if nameRow[6] == lastName:
						row[3] = nameRow[3]  # title
						row[4] = nameRow[4]  # Herr / Frau
						row[5] = nameRow[5]  # first name
						lastNameFound = True
						break

				if lastNameFound == False:
					print(lastName + " not found in EvaSys export --> needs to be updated manually")

			outputWriter.writerow(rowNew)
