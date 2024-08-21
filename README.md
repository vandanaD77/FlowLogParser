# FlowLogParser README

## Overview
This Flow Log Parser processes flow logs by analyzing the destination port and protocol number to identify specific tags as defined in a lookup table. The parser produces:
1. Tag Counts
2. Port/Protocol Combination Counts

## Assumptions:
1. The program supports default log format of AWS VPC flow logs. The program assumes that the "dstport" is the 7th field (index 6) and the "protocol" is the 8th field (index 7) in each line of the flow logs. These positions are fixed based on the default format. To make the FlowLogParser compatible with a custom log format, the indices for the dstport and protocol fields can be modified according to the specific format defined in the custom log format.
2. The flow logs file is a plain text file and it should have fields separated by whitespace.
3. The lookup table file and protocol numbers file are in CSV format. Imported protocol numbers file from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml.
4. If a protocol number does not have a corresponding keyword in the protocol numbers file, it is assigned the keyword 'Unassigned'.
5.  If a port/protocol combination is not found in the lookup table, it is tagged as 'Untagged'.

## Prerequisites:
- Install Python 3.x

## To run the program:
1.  Ensure the following files are available:
    (a) Flow logs (flowlogs.txt)
    (b) Lookup table (lookup_table.csv)
    (c) Protocol numbers (protocol_numbers.csv)
    Also, provide the path to the file where the output needs to be saved.
    Provide the path to these files in Lines 91-94 in flow_log_parser.py respectively. 
    ```python
    lookup_table_file = 'lookup_table.csv'
    flow_logs_file = 'flowlogs.txt'
    protocol_file = 'protocol_numbers.csv'
    output_file = 'output.txt'
    ```
2. Custom Format Adjustment:
    If using a custom log format, update the field indices in Lines 17, 18 in `flow_log_parser.py`:
     ```python
     self.dstport_index = <new_dstport_index>
     self.protocol_number_index = <new_protocol_index>
     ```
3.  Run the script from the command line:
     ```bash
     python flow_log_parser.py
     ```
    The output will be saved in `output.txt`.

## Handling of Requirements

1. Flow Log File Size (up to 10 MB):
   - The program reads the flow logs file line by line to handle large files efficiently. This approach allows the parser to process files up to 10 MB in size without running into memory issues.

2. Lookup File with up to 10,000 Mappings:
   - The lookup table file can contain up to 10,000 mappings. The parser loads these mappings into a dictionary, which provides efficient access during the flow log parsing process.

3. Multiple Port/Protocol Combinations for Tags:
   - Tags in the lookup table can map to more than one port/protocol combination. The parser handles this by storing each port/protocol combination as a key in a dictionary, mapping to its corresponding tag.

4. Case Insensitive Matching:
   - All matching operations between flow logs and the lookup table are case insensitive. This is accomplished by converting all relevant strings (ports, protocols, tags) to lowercase before performing any comparisons.


## Testing
Tested Scenarios: 
1. Valid input files
2. Missing protocol entries
3. Unmatched tags
4. Custom formats with varying field orders
