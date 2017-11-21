# Tf Testrunner

tf-testrunner parses [Terraform configuration](https://www.terraform.io/docs/configuration/index.html) to Python and then runs your tests.

### How it works:

Testrunner automates the output of the command ```terraform plan```, saves its output to a temp directory. Parses the temp file to a Python dict object and then runs your test folder against it. 

Refer to the [examples directory](https://github.com/UKHomeOffice/tf-testrunner/tree/master/examples/basic-proof) for example Terraform projects that use [tf-testrunner](https://github.com/UKHomeOffice/tf-testrunner/). 

## Requirements

- [Python](https://github.com/python) **(~> 3.6.3)**

- [Docker](https://github.com/docker) **(~> 1.13)**

- [Drone](https://github.com/drone/drone) **(~> 0.8)**

## Installation

tf-testrunner is packaged as a Docker container image on [Quay](https://github.com/coreos/quay-docs), it can be [run via Drone](https://github.com/drone/drone).

### Adding tf-testrunner to a Terraform project:

Once the requirements listed above have been installed, add the ```drone.yml``` configuration file to the project's root:

```
pipeline:

  test:
    image: quay.io/ukhomeofficedigital/tf-testrunner
    commands: python -m unittest tests/*_test.py
```

Then, run Drone in root to launch:
```
drone5 exec
```

Refer to the [examples directory](https://github.com/UKHomeOffice/tf-testrunner/tree/master/examples/basic-proof) for example Terraform projects that use [tf-testrunner](https://github.com/UKHomeOffice/tf-testrunner/). 

## Tf Testrunner uses

* [tfjson](https://github.com/palantir/tfjson)






