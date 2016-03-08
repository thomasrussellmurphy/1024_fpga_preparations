#!/usr/bin/env python

import csv
import io
import os
import sys

# Constants for accessing CSV dict
DEVICE_PIN_KEY = '5CGXFC5C6F27C7N Pin'
PIN_DIRECTION_KEY = 'FPGA Pin Direction'
IO_STANDARD_KEY = 'I/O Standard'
HDL_NAME_KEY = 'HDL Name'

# String constant for generating Quartus Setting File snippet
PIN_ASSIGNMENT_TEMPLATE = '''set_location_assignment {pin} -to {signal}
set_instance_assignment -name IO_STANDARD "{standard}" -to {signal}'''

def main():
  # Usage: `python create_template_snippets.py "Source Data.csv"`
  if len(sys.argv) is not 2:
    # Improper arguments given, exit with an error
    print("Provide source CSV path as only argument")
    sys.exit(1)

  source_path_str = sys.argv[1]

  print("Attempting to work with source CSV: " + source_path_str)
  if not os.path.isfile(sys.argv[1]):
    print("Source CSV path does not exist.")
    sys.exit(2)

  source_path = os.path.abspath(source_path_str)

  with open(source_path, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      assignment = PIN_ASSIGNMENT_TEMPLATE.format(
        pin = row[DEVICE_PIN_KEY],
        signal = row[HDL_NAME_KEY],
        standard = row[IO_STANDARD_KEY])
      print(assignment)

# Call the main() function to begin the program.
if __name__ == "__main__":
  main()
