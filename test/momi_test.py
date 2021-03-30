import pytest
from assertpy import assert_that
import momi as momimomi
from unittest.mock import patch
from pyVmomi import vim


class TestTrafficRule:
    def test_set(self):
        rule = momimomi.TrafficRule()
        rule.set_rule(
            desc='desc1',
            src='192.168.1.1/32',
            dst='192.168.2.1/32',
            srcport='5000',
            dstport='80',
            protocol='tcp',
            action='accept'
        )
        assert_that(rule.desc).is_equal_to('desc1')
        assert_that(rule.src).is_equal_to('192.168.1.1/32')
        assert_that(rule.dst).is_equal_to('192.168.2.1/32')
        assert_that(rule.desc).is_equal_to('desc1')

        assert_that(rule.to_trafficRule().__class__.__name__).is_equal_to('vim.dvs.TrafficRule')


class TestMomi:
    @pytest.fixture(scope='function', autouse=True)
    def pgobj(self):
        with patch('momi.get_obj') as m:
            m.return_value = []
            yield m

    @pytest.fixture(scope='function', autouse=True)
    def sample_rules(self):
        rules = {}
        rules['rule1'] = dict(
            desc='desc1',
            src='192.168.1.1/32',
            dst='192.168.2.1/32',
            srcport='5000',
            dstport='80',
            protocol='tcp',
            action='accept'
        )
        rules['rule2'] = dict(
            desc='desc2',
            src='192.168.1.1/32',
            dst='192.168.2.1/32',
            srcport='5000',
            dstport='80',
            protocol='tcp',
            action='accept'
        )
        yield rules

    @pytest.fixture(scope='function', autouse=True)
    def trafficruleset(self, sample_rules):
        with patch('momi.getTrafficRuleSet') as m:
            ruleset = vim.dvs.TrafficRuleset()
            ruleset.enabled = True

            rule = momimomi.TrafficRule()
            rule.set_rule(**sample_rules['rule1'])
            ruleset.rules.append(rule)
            
            rule = momimomi.TrafficRule()
            rule.set_rule(**sample_rules['rule2'])
            ruleset.rules.append(rule)
            
            m.return_value = ruleset
            yield m

    def test_load_and_create_and_to_trafficruleset(self, sample_rules):
        content = None
        momi = momimomi.Momi(content)
        momi.load(pgname='pg01')
        momi.clear_rule()
        momi.enabled = True
        momi.add_rule(**sample_rules['rule1'])
        momi.add_rule(**sample_rules['rule2'])
        assert_that(momi.rules).is_length(2)
        assert_that(momi.rules[0].desc).is_equal_to(sample_rules['rule1']['desc'])

        trafficruleset = momi.to_toTrafficRuleSet()
        assert_that(trafficruleset.rules).is_length(2)
        
