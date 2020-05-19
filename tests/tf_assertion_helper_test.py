# pylint: disable=missing-docstring, line-too-long, protected-access
import unittest
from tf_assertion_helper import finder, get_value


class TestFinder(unittest.TestCase):
    def setUp(self):
        self.snippet = {
            'egress.482069346.cidr_blocks.#': '1',
            'egress.482069346.cidr_blocks.0': '0.0.0.0/0',
            'egress.482069346.description': '',
            'egress.482069346.from_port': '0',
            'egress.482069346.ipv6_cidr_blocks.#': '0',
            'egress.482069346.prefix_list_ids.#': '0',
            'egress.482069346.protocol': '-1',
            'egress.482069346.security_groups.#': '0',
            'egress.482069346.self': 'false',
            'egress.482069346.to_port': '0',
            'id': '',
            'ingress.#': '2',
            'ingress.244708223.cidr_blocks.#': '1',
            'ingress.244708223.cidr_blocks.0': '0.0.0.0/0',
            'ingress.244708223.description': '',
            'ingress.244708223.from_port': '3389',
            'ingress.244708223.ipv6_cidr_blocks.#': '0'
        }

    def test_happy_path(self):
        self.assertTrue(finder(self.snippet, 'ingress', {'cidr_blocks.0': '0.0.0.0/0', 'from_port': '3389'}))

    def test_unhappy_path(self):
        self.assertFalse(finder(self.snippet, 'ingress', {'cidr_blocks.0': '0.0.0.0/0', 'from_port': '0', 'self': 'true'}))


class TestGetValue(unittest.TestCase):
    def setUp(self):
        self.snippet = {
            "format_version": "0.1",
            "terraform_version": "0.12.25",
            "planned_values": {},
            "resource_changes": [{
                "address": "module.rds_alarms.aws_cloudwatch_log_group.lambda_log_group_slack",
                "module_address": "module.rds_alarms",
                "mode": "managed",
                "type": "aws_cloudwatch_log_group",
                "name": "lambda_log_group_slack",
                "provider_name": "aws",
                "change": {
                    "actions": [
                        "create"
                    ],
                    "before": "None",
                    "after": {
                        "kms_key_id": "None",
                        "name": "/aws/lambda/foo-lambda-slack-notprod",
                        "name_prefix": "None",
                        "retention_in_days": 14,
                        "tags": {
                            "Name": "lambda-log-group-slack-1234-apps"
                        }
                    },
                    "after_unknown": {
                        "arn": "blah",
                        "id": "blah",
                        "tags": {}
                    }
                }
            }]
        }

    def test_happy_path(self):
        self.assertEqual(get_value(self.snippet, "module.rds_alarms.aws_cloudwatch_log_group.lambda_log_group_slack", "retention_in_days"), 14)

    def test_unhappy_path(self):
        self.assertNotEqual(get_value(self.snippet, "module.rds_alarms.aws_cloudwatch_log_group.lambda_log_group_slack", "kms_key_id"), "something_not_there")


if __name__ == '__main__':
    unittest.main()
