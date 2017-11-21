# Tf Testrunner
[![Docker Repository on Quay](https://quay.io/repository/ukhomeofficedigital/tf-testrunner/status "Docker Repository on Quay")](https://quay.io/repository/ukhomeofficedigital/tf-testrunner)

tf-testrunner parses [Terraform configuration](https://www.terraform.io/docs/configuration/index.html) to Python and then runs your tests.

### How it works:

Testrunner automates the output of the command ```terraform plan```, saves its output to a temp directory. Parses the temp file to a Python dict object and then runs your test folder against it. 

Refer to the [examples directory](https://github.com/UKHomeOffice/tf-testrunner/tree/master/examples/basic-proof) for example Terraform projects that use [tf-testrunner](https://github.com/UKHomeOffice/tf-testrunner/). 


## Usage

### CI (Drone ~> 0.5) execution
Add a build step
```yaml
  test:
    image: quay.io/ukhomeofficedigital/tf-testrunner
    commands: python -m unittest tests/*_test.py
``````
```shell
drone exec
```

### Docker (~> 1.13) in-situ execution
```shell
docker run --rm -v `pwd`:/mytests -w /mytests quay.io/ukhomeofficedigital/tf-testrunner
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
    def setUp(self):
        self.snippet = """
            provider "aws" {
              region = "eu-west-2"
              profile = "foo"
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

**[More examples](./examples)**

## Acknowledgements

We leverage [tfjson](https://github.com/palantir/tfjson) to get a machine readable output of the `terraform plan` which we can then evaluate against, When terraform has an inbuilt [machine readable output](https://github.com/hashicorp/terraform/pull/3170), expect a refactor of this tool to use that instead of tfjson.
