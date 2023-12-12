# pylint: disable=missing-docstring, line-too-long, protected-access
import unittest
from runner import Runner


class TestE2E(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.snippet = """
            provider aws {
              region = "eu-west-2"
              access_key = "foo"
              secret_key = "bar"
              skip_credentials_validation = true
              skip_requesting_account_id = true
            }

            module "my_module" {
              source = "./mymodule"
            }

        """
        self.runner = Runner(self.snippet)
        self.result = self.runner.result

    def test_terraform_version(self):
        print(self.result)
        self.assertEqual(self.result["terraform_version"], "1.6.5")

    def test_root_module(self):
        self.assertEqual(self.result["configuration"]["root_module"]["module_calls"]["my_module"]["source"], "./mymodule")

    def test_instance_type(self):
        self.assertEqual(self.runner.get_value("module.my_module.aws_instance.foo", "instance_type"), "t2.micro")

    def test_ami(self):
        self.assertEqual(self.runner.get_value("module.my_module.aws_instance.foo", "ami"), "foo")


if __name__ == '__main__':
    unittest.main()
