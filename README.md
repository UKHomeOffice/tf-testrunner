# Tf Testrunner

tf-testrunner parses [Terraform configuration](https://www.terraform.io/docs/configuration/index.html) to Python, readying it for testing.

### How it works:

Automating the output of the command ```terraform plan```, saving it's output to a temp directory and parsing it to a Python dict object to then run unit tests against. 

Refer to the [examples directory](https://github.com/UKHomeOffice/tf-testrunner/tree/master/examples/basic-proof) for example Terraform projects that use [tf-testrunner](https://github.com/UKHomeOffice/tf-testrunner/). 

## Requirements

- [Python](https://github.com/python) **(~> 3.6.3)**

- [Docker](https://github.com/docker) **(~> 1.13)**

- [Drone](https://github.com/drone/drone) **(~> 0.8)**

## Installation

tf-testrunner is packaged as a Docker container image on [Quay](https://github.com/coreos/quay-docs), it can be [installed via Drone](https://github.com/drone/drone).

### Adding tf-testrunner to a Terraform project:

Once the requirements listed above have been installed, add the ```drone.yml``` configuration file to the project's root:

```
pipeline:

  test:
    image: quay.io/ukhomeofficedigital/tf-testrunner
    commands: python -m unittest tests/*_test.py
```

Then, run Drone to launch the tests:
```
basic-proof ottern$ drone5 exec
```

Refer to the [examples directory](https://github.com/UKHomeOffice/tf-testrunner/tree/master/examples/basic-proof) for example Terraform projects that use [tf-testrunner](https://github.com/UKHomeOffice/tf-testrunner/). 

### Tf Testrunner uses

* [tfjson](https://github.com/palantir/tfjson)






