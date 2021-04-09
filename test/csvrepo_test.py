import pytest
from assertpy import assert_that
import momi.csvrepo as csvrepo
from unittest.mock import patch
from pyVmomi import vim

class xTestRuleStoreValidator:
    def test_1(self):
        schema2 = {
            "key1": {
                "type": ["float", "list"],
                "min": 0,
                "max": 1,
                "check_with": "sum_eq_one"
            },
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
            }
        }
        v = csvrepo.RuleStoreValidator(schema2)
        v.validate({
            "key1": 1,
            "description": "",
            "action": "accept",
            "source_ip": '1.1.1.1/24',
            "destination_ip": "2.2.2f.2/24"
        })
        assert v.errors == {}

class xTestRuleStore:
    def test_1(self):
        store = csvrepo.RuleStore()
        store.load('test/fixture/pg01.csv')
        store.dcname = 'dc01'
        store.pgname = 'pg01'
        store.rules[0]['description'] = 'abcd'

        assert store.rules[0] == dict(
            description='abcd',
            source_ip='192.168.11.1/32',
            destination_ip='192.168.12.1/32',
            source_port='ANY',
            destination_port='ANY',
            protocol='ANY',
            action='',
            comment='cmt'
        )

        actual = store._save(format=True)
        print(store.rules)
        expect = [
            "dcname: dc01\n",
            "pgname: pg01\n",
            "---\n",
            "description , action , source_ip       , destination_ip  , source_port , destination_port , protocol , comment\n",
            "abcd        ,        , 192.168.11.1/32 , 192.168.12.1/32 , ANY         , ANY              , ANY      , cmt\n",
            "efgh        ,        , 192.168.11.1/32 , 192.168.12.1/32 , ANY         , ANY              , ANY      , \n",
        ]
        assert actual[0] == expect[0]
        assert actual[1] == expect[1]
        assert actual[2] == expect[2]
        assert actual[3] == expect[3]
        assert actual[4] == expect[4]
        assert actual[5] == expect[5]
        