# pylint: disable=missing-docstring, line-too-long, protected-access
import unittest
from runner import Runner


class TestE2E(unittest.TestCase):
    def setUp(self):
        self.snippet = """
            provider "aws" {
              region = "eu-west-2"
              access_key = "foo"
              secret_key = "bar"
              skip_credentials_validation = true
              skip_get_ec2_platforms = true
            }
            
            module "my_module" {
              source = "./mymodule"
            }

        """
        self.result = Runner(self.snippet).result

    def test_root_destroy(self):
        print (self.result)
        self.assertEqual(self.result["destroy"], False)

    def test_instance_type(self):
        self.assertEqual(self.result['my_module']["aws_instance.foo"]["instance_type"], "t2.micro")

    def test_ami(self):
        self.assertEqual(self.result['my_module']["aws_instance.foo"]["ami"], "foo")

    def test_destroy(self):
        self.assertEqual(self.result['my_module']["aws_instance.foo"]["destroy"], False)

    def test_destroy_tainted(self):
        self.assertEqual(self.result['my_module']["aws_instance.foo"]["destroy_tainted"], False)


if __name__ == '__main__':
    unittest.main()
