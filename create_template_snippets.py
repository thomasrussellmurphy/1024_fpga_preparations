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
SW_RATE_KEY = "Max Switching Rate"
RESISTOR_STATE_KEY = "Weak Pull Up Resistor"

# String constant for generating Quartus Setting File snippet
PIN_ASSIGNMENT_TEMPLATE = '''set_location_assignment {pin} -to {signal}
set_instance_assignment -name IO_STANDARD "{standard}" -to {signal}
'''
TOGGLE_RATE_ASSIGNMENT_TEMPLATE='''set_instance_assignment -name IO_MAXIMUM_TOGGLE_RATE "{rate}" -to {signal}
'''
MODULE_HEADER_TEMPLATE = '''{direction} {name},
'''
PULL_UP_RESISTOR_TEMPLATE = '''set_instance_assignment -name WEAK_PULL_UP_RESISTOR {state} -to {pin}

'''

# Constants for filename manipulation
CSV_EXTENSION_LOWER = '.csv'
ASSIGNMENTS_SUFFIX = '-QSF_ASSIGNMENTS_OUT.txt'
HEADERS_SUFFIX = '-VERILOG_HEADER_OUT.txt'

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

  assignments = []
  headers = []

  with open(source_path, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      pin_assign = PIN_ASSIGNMENT_TEMPLATE.format(
        pin = row[DEVICE_PIN_KEY],
        signal = row[HDL_NAME_KEY],
        standard = row[IO_STANDARD_KEY])
      header = MODULE_HEADER_TEMPLATE.format(
        direction = row[PIN_DIRECTION_KEY],
        name = row[HDL_NAME_KEY])
      sw_rate = TOGGLE_RATE_ASSIGNMENT_TEMPLATE.format(
        rate = row[SW_RATE_KEY],
        signal = row[HDL_NAME_KEY])
      res_state = PULL_UP_RESISTOR_TEMPLATE.format(
        state = row[RESISTOR_STATE_KEY],
        pin = row[DEVICE_PIN_KEY])

      # Text to be output
      # QSF assignments are pin naming, toggle rate, resistor state
      # Headers are material to put in Verilog top level
      assignments.append(pin_assign)
      assignments.append(sw_rate)
      assignments.append(res_state)
      headers.append(header)

  output_base_path_str = source_path_str

  if output_base_path_str.lower().endswith(CSV_EXTENSION_LOWER):
    output_base_path_str = output_base_path_str[:-4]

  output_assignments_path_str = output_base_path_str + ASSIGNMENTS_SUFFIX
  output_headers_path_str = output_base_path_str + HEADERS_SUFFIX

  print('Clobbering ' + output_assignments_path_str)
  output_assignments_path = os.path.abspath(output_assignments_path_str)

  with open(output_assignments_path, 'w') as output:
    output.writelines(assignments)

  print('Clobbering ' + output_headers_path_str)
  output_headers_path = os.path.abspath(output_headers_path_str)

  with open(output_headers_path, 'w') as output:
    output.writelines(headers)

# Call the main() function to begin the program.
if __name__ == "__main__":
  main()
