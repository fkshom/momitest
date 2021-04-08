import pytest
from assertpy import assert_that
import momi.csvrepo as csvrepo
from unittest.mock import patch
from pyVmomi import vim
import pytest_diff

class TestRuleStore:
    def test_1(self):
        store = csvrepo.RuleStore()
        store.load('test/fixture/pg01.csv')
        store.dcname = 'dc01'
        store.pgname = 'pg01'
        store.rules[0]['description'] = 'abcd'

        assert_that(store.rules[0]).is_equal_to(dict(
            description='abcd',
            source_ip='192.168.11.1/32',
            destination_ip='192.168.12.1/32',
            source_port='ANY',
            destination_port='ANY',
            protocol='ANY',
            action='',
            comment='cmt'
        ))

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
        assert_that(actual[0]).is_equal_to(expect[0])
        assert_that(actual[1]).is_equal_to(expect[1])
        assert_that(actual[2]).is_equal_to(expect[2])
        assert_that(actual[3]).is_equal_to(expect[3])
        assert_that(actual[4]).is_equal_to(expect[4])
        assert_that(actual[5]).is_equal_to(expect[5])
        