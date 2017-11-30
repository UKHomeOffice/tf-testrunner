# pylint: disable=missing-docstring, line-too-long, protected-access
import unittest
from tf_assertion_helper import finder


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


if __name__ == '__main__':
    unittest.main()
