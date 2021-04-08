from pprint import pprint as pp
import re

RULE_LABELS = "description,action,source_ip,destination_ip,source_port,destination_port,protocol,comment".split(',')

class RuleStore():
    def __init__(self):
        self.rules = []

    def load(self, filename):
        lines = None
        with open(filename) as f:
            lines = f.readlines()    
    
        # read meta area
        while True:
            line = lines.pop(0).rstrip()
            m = re.match(r'---+', line)
            if m:
                break

            if line.startswith('dcname'):
                self.dcname = line.split(':', 2)[1].strip()
                continue
            elif line.startswith('pgname'):
                self.pgname = line.split(':', 2)[1].strip()
            else:
                raise Exception(f'Unknown meta data: {line}')

        # read header
        headers = list(map(lambda col: col.strip(), lines.pop(0).split(',')))

        # read data
        for line in lines:
            values = list(map(lambda col: col.strip(), line.strip().split(',')))
            self.rules.append(dict(zip(headers, values)))

    def _save(self, format=True):
        meta = []
        meta.append(f'dcname: {self.dcname}' + "\n")
        meta.append(f'pgname: {self.pgname}' + "\n")
        meta.append(f'---' + "\n")

        # prepare header
        data = []
        data.append(RULE_LABELS)

        # prepate data
        for rule in self.rules:
            data.append(rule.values())

        # calculate column size
        data_t = list(zip(*data))
        widths = list(map(lambda val: len(val), [max(cols, key=len) for cols in data_t]))

        data2 = []
        for row_num, row in enumerate(data):
            new_row = []
        
            for val, width, col_name in zip(row, widths, RULE_LABELS):
                val = val.ljust(width)
                if col_name == 'comment':
                    val = val.strip()
                new_row.append(val)
                        
            line = ' , '.join(new_row) + "\n"
            data2.append(line)

        return meta + data2

    def save(self, filename, format=True):
        data = self._save(format)

        with open(filename, 'w') as f:
            f.writelines(data)



