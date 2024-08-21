import csv
from collections import defaultdict
from io import StringIO

class FlowLogParser:
    def __init__(self, flowlogs_path, lookup_table_path, protocol_numbers_path):
        # Assert that files have the correct extensions
        assert flowlogs_path.endswith('.txt'), "Flow logs file must end with .txt"
        assert lookup_table_path.endswith('.csv'), "Lookup table file must end with .csv"
        assert protocol_numbers_path.endswith('.csv'), "Protocol numbers file must end with .csv"

        self.flow_logs_file = flowlogs_path
        self.lookup_table_file = lookup_table_path
        self.protocol_numbers_file = protocol_numbers_path

        # Fixed indices for dstport and protocol_number
        self.dstport_index = 6
        self.protocol_number_index = 7
    
    def protocol_lookup_table(self):
        protocol_dict = {}

        with open(self.protocol_numbers_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                protocol_keyword = row['Keyword'].strip()
                protocol_dict[row['Decimal']] = protocol_keyword if protocol_keyword else 'Unassigned'
                
        return protocol_dict

    def load_lookup_table(self):
        lookup_table = {}
        with open(self.lookup_table_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                key = (row['dstport'].strip(), row['protocol'].strip().lower())
                lookup_table[key] = row['tag'].strip()
        return lookup_table

    def parse_flow_logs(self):
        lookup_table = self.load_lookup_table()
        protocol_dict = self.protocol_lookup_table()

        tag_counter = defaultdict(int)
        port_protocol_counter = defaultdict(int)

        with open(self.flow_logs_file, 'r') as file:
            for line in file:
                parts = line.split()
                dstport = parts[self.dstport_index].strip()
                protocol = protocol_dict[parts[self.protocol_number_index].strip()].lower()
                
                # Count port/protocol combination
                port_protocol_counter[(dstport, protocol)] += 1

                # Match tag using lookup table
                tag = lookup_table.get((dstport, protocol), 'Untagged')
                tag_counter[tag] += 1

        return tag_counter, port_protocol_counter

    def generate_output(self, tag_counter, port_protocol_counter):
        output = StringIO()
        
        # Write tag counts
        output.write('Tag Counts:\n')
        output.write('Tag,Count\n')
        for tag, count in sorted(tag_counter.items()):
            output.write(f'{tag},{count}\n')

        output.write('\n')

        # Write port/protocol combination counts
        output.write('Port/Protocol Combination Counts:\n')
        output.write('Port,Protocol,Count\n')
        for (port, protocol), count in sorted(port_protocol_counter.items()):
            output.write(f'{port},{protocol},{count}\n')

        output_str = output.getvalue()
        output.close()
        return output_str

    def write_output_to_file(self, output_filename):
        tag_counter, port_protocol_counter = self.parse_flow_logs()
        output_str = self.generate_output(tag_counter, port_protocol_counter)

        with open(output_filename, 'w') as file:
            file.write(output_str)

def main():
    lookup_table_file = 'lookup_table.csv'
    flow_logs_file = 'flowlogs.txt'
    protocol_file = 'protocol_numbers.csv'
    output_file = 'output.txt'

    parser = FlowLogParser(flow_logs_file, lookup_table_file, protocol_file)
    parser.write_output_to_file(output_file)

if __name__ == '__main__':
    main()