from attr.setters import pipe
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from pprint import pprint as pp

def get_obj(content, obj, name):
    return None

def getTrafficRuleSet(pg):
    return None

class TrafficRule:
    def __init__(self):
        self._trafficrule = None

    def _prim_to_ipaddr(self, value):
        tmp = vim.SingleIp()
        tmp.address = value
        return tmp

    def _ipaddr_to_prim(self, obj):
        return obj.address

    def _prim_to_port(self, value):
        tmp = vim.dvs.TrafficRule.SingleIpPort()
        tmp.portNumber = int(value)
        return tmp

    def _prim_to_protocol(self, value):
        tmp = vim.IntExpression()
        if value == 'tcp':
            value = 6
        elif value == 'udp':
            value = 17

        tmp.value = value
        return tmp

    def set_rule(self, desc, src, dst, srcport, dstport, protocol, action):
        tmp = vim.dvs.TrafficRule()
        tmp.action = vim.dvs.TrafficRule.AcceptAction()
        tmp.direction = 'both'
        tmp.description = desc

        qual = vim.dvs.TrafficRule.IpQualifier()
        qual.sourceAddress = self._prim_to_ipaddr(src)
        qual.destinationAddress = self._prim_to_ipaddr(dst)
        qual.sourceIpPort = self._prim_to_port(srcport)
        qual.destinationIpPort = self._prim_to_port(dstport)
        qual.protocol = self._prim_to_protocol(protocol)
        qual.tcpFlags = None

        tmp.qualifier.append(qual)

        self._trafficrule = tmp

    def load_rule(self, trafficrule):
        self._trafficrule = trafficrule

    def to_trafficRule(self):
        return self._trafficrule

    @property
    def desc(self):
        return self._trafficrule.description

    @property
    def src(self):
        return self._ipaddr_to_prim(self._trafficrule.qualifier[0].sourceAddress)

    @property
    def dst(self):
        return self._ipaddr_to_prim(self._trafficrule.qualifier[0].destinationAddress)

class Momi:
    def __init__(self, content):
        self.content = content
        self.rules = []
        self.enabled = None
 
    def clear_rule(self):
        self.rules = []

    def add_rule(self, **kwargs):
        rule = TrafficRule()
        rule.set_rule(**kwargs)
        self.rules.append(rule)
    
    def load(self, pgname: str):
        pg = get_obj(self.content, pgname)
        ruleset = getTrafficRuleSet(pg)
        self.enabled = ruleset.enabled
        self.rules = ruleset.rules

    def to_toTrafficRuleSet(self):
        tmp = vim.dvs.TrafficRuleset()
        tmp.enabled = self.enabled
        tmp.rules = [rule.to_trafficRule() for rule in self.rules]
        return tmp

