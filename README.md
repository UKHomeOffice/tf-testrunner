# Tf Testrunner
[![Docker Repository on Quay](https://quay.io/repository/ukhomeofficedigital/tf-testrunner/status "Docker Repository on Quay")](https://quay.io/repository/ukhomeofficedigital/tf-testrunner)

tf-testrunner parses [Terraform configuration](https://www.terraform.io/docs/configuration/index.html) to Python and then runs your tests.

Current terraform upgrade tag is 32.

### How it works:

Testrunner automates the output of the command ```terraform plan```, saves its
output to a temp directory. Parses the temp file to a Python dict object and
then runs your test folder against it.

Refer to the [examples
directory](https://github.com/UKHomeOffice/tf-testrunner/tree/master/examples/basic-proof)
for example Terraform projects that use
[tf-testrunner](https://github.com/UKHomeOffice/tf-testrunner/).


## Usage

### CI (Drone ~> 0.5) execution
Add a build step
```yaml
  test:
    image: quay.io/ukhomeofficedigital/tf-testrunner:32
    commands: python -m unittest tests/*_test.py
``````
```shell
drone exec
```

### Docker (~> 1.13) in-situ execution
```shell
docker run --rm -v `pwd`:/mytests -w /mytests quay.io/ukhomeofficedigital/tf-testrunner:32
```

### Python (\~> 3.6.3) & Go (\~> 1.9.2) execution
```bash
pip install git+git://github.com/UKHomeOffice/tf-testrunner.git#egg=tf-testrunner
go get github.com/wybczu/tfjson
```

### Test authoring
```shell
mkdir tests
touch tests/__init__.py
```
tests/my_test.py
```python
# pylint: disable=missing-docstring, line-too-long, protected-access
import unittest
from runner import Runner

class TestMyModule(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.snippet = """
            provider "aws" {
              region = "eu-west-2"
              access_key = "foo"
              secret_key = "bar"
              profile = "foo"
              skip_credentials_validation = true
              skip_get_ec2_platforms = true
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
        self.assertEqual(self.result["terraform_version"], "0.12.25")

    def test_root_module(self):
        self.assertEqual(self.result["configuration"]["root_module"]["module_calls"]["my_module"]["source"], "./mymodule")

    def test_instance_type(self):
        self.assertEqual(self.runner.get_value("module.my_module.aws_instance.foo", "instance_type"), "t2.micro")

    def test_ami(self):
        self.assertEqual(self.runner.get_value("module.my_module.aws_instance.foo", "ami"), "foo")


if __name__ == '__main__':
    unittest.main()
```
my_module.tf
```hcl-terraform
resource "aws_instance" "foo" {
  ami           = "foo"
  instance_type = "t2.micro"
}
```

**[More examples](aws_terraform_test_runner/examples)**

## Additional Usage Method get_value

To handle the terraform output plan of json [structure](https://www.terraform.io/docs/internals/json-format.html), we are only interested in ``resource_changes`` sections with arrays of resources to be changed. Helper method  ```get_vaule``` will get first parmater of module resource name and its change value in second parameter.
See example snippet.

tests/tf_assertion_helper_test.py
```hcl-terraform
import unittest
from tf_assertion_helper import get_value

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

```


## Additional Usage Method finder

To handle the occurrence of unique numbers in keys after parsing, use the assertion helper method ```finder```.

tests/tf_assertion_helper_test.py
```hcl-terraform
import unittest
from runner import Runner

parent = {
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

class TestFinder(unittest.TestCase):

    def test_happy_path(self):
        self.assertTrue(Runner.finder(parent, 'ingress', {'cidr_blocks.0': '0.0.0.0/0', 'from_port': '3389'}))

    def test_unhappy_path(self):
        self.assertFalse(Runner.finder(parent, 'ingress', {'cidr_blocks.0': '0.0.0.0/0', 'from_port': '0', 'self': 'true'}))


if __name__ == '__main__':
    unittest.main()
```

## Acknowledgements

*UPDATE TF12*

Following [tfjson](https://github.com/palantir/tfjson) is no longer support for terraform 12. This is the reason terraform 12 can only use default output of terraform plan in json format. [Use terraform show -json planned_file](https://www.terraform.io/docs/internals/json-format.html)

*OLD TF11*

We leverage [tfjson](https://github.com/palantir/tfjson) to get a machine
readable output of the `terraform plan` which we can then evaluate against.
When terraform has an inbuilt [machine readable
output](https://github.com/hashicorp/terraform/pull/3170), expect a refactor of
this tool to use that instead of tfjson.

When researching testing strategies for Terraform, we found [Carlos Nunez](https://github.com/carlosonunez)'s article [Top 3 Terraform Testing Strategies...](https://www.contino.io/insights/top-3-terraform-testing-strategies-for-ultra-reliable-infrastructure-as-code) to be great inspiration and very informative.
