from pprint import pprint as pp
import re
import cerberus

RULE_LABELS = "description,action,source_ip,destination_ip,source_port,destination_port,protocol,comment".split(',')

decimal_type = cerberus.TypeDefinition('decimal', (str,), ())

class RuleStoreValidator(cerberus.Validator):
    def __init__(self):
        super().__init__()
        self.schema = {
            "description": {
                "type": 'string'
            },
            "action": {
                "type": 'string',
                "allowed": ["accept", "drop", ""]
            },
            "source_ip": {
                "type": "string",
                "check_with": "ipaddr"
            },
            "destination_ip": {
                "type": "string",
                "check_with": "ipaddr"
            },
            "source_port": {
                "type": "string",
                "regex": r"\d+|\d+-\d+"
            },
            "destination_port": {
                "type": "string",
                "regex": r"\d+|\d+-\d+"
            },
            "protocol": {
                "type": "string",
                "allowed": ["tcp", "ucp", "arp", "any"]
            }
        }
        self.require_all = True
        self.allow_unknown = False
    
    def _check_with_ipaddr(self, field, value):
        if not re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}|ANY", value):
            self._error(field, f"'{field}' must be x.x.x.x/x or ANY")

class RuleStore():
    def __init__(self):
        self.rules = []

    def validate(self):
        v = RuleStoreValidator()
        v.validate(self.__dir__)
        if v.errors:
            pp(v.errors)
            raise ""


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



