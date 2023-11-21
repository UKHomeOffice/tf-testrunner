# pylint: disable=missing-docstring, line-too-long, protected-access
import unittest
from unittest import mock
from runner import Runner


class TestRunnerMethods(unittest.TestCase):
    def setUp(self):
        self.snippet = "string"
        self.tmpdir = "foo"

    @mock.patch("tempfile.mkdtemp")
    def test_mktmpdir(self, tempfile_mock):
        tempfile_mock.return_value = "path"
        Runner._mktmpdir(self)
        self.assertEqual(self.tmpdir, "path")

    @unittest.skip  # @TODO
    def test_run(self):
        # runner.run()
        self.assertEqual('{dict}', '{dict}')

    @mock.patch("shutil.rmtree")
    def test_removetmpdir(self, shutil_mock):
        Runner._removetmpdir(self)
        shutil_mock.assert_called_once_with(self.tmpdir)

    @mock.patch("subprocess.call")
    def test__terraform_init(self, subprocess_mock):
        Runner._terraform_init(self)
        subprocess_mock.assert_called_once_with(["terraform", f"-chdir={self.tmpdir}", "init"])

    @mock.patch("os.system")
    def test_teraform_plan(self, os_mock):
        Runner._terraform_plan(self)
        os_mock.assert_called_once_with(
            f"terraform -chdir={self.tmpdir} plan -input=false -out={self.tmpdir}/mytf.tfplan")

    @unittest.skip  # @TODO
    @mock.patch("os.system")
    def test__copy_tf_files(self, os_mock):
        Runner._copy_tf_files(self)
        os_mock.assert_any_call("rm -rf .terraform/modules")
        os_mock.assert_any_call("mkdir " + self.tmpdir + "/mymodule")

    @mock.patch("subprocess.check_output")
    def test_snippet_to_json(self, subprocess_mock):
        Runner.snippet_to_json(self)
        subprocess_mock.assert_called_once_with(
            ["terraform", f"-chdir={self.tmpdir}", "show",
             "-no-color", "-json", f"{self.tmpdir}/mytf.tfplan"])

    @mock.patch("json.loads")
    def test_json_to_dict(self, mock_json):
        mock_json.return_value = {}
        json_file = {}
        self.assertEqual(Runner.json_to_dict(json_file), {})


class TestE2E(unittest.TestCase):
    def setUp(self):
        self.snippet = """
        provider "aws" {
            region  = "eu-west-2"
            access_key = "foo"
            secret_key = "bar"
            skip_credentials_validation = true
            skip_requesting_account_id = true
        }

        resource "aws_instance" "foo" {
          ami           = "foo"
          instance_type = "t2.micro"
        }
        """
        self.runner = Runner(self.snippet)
        self.result = self.runner.result

    def test_terraform_version(self):
        print(self.result)
        self.assertEqual(self.result["terraform_version"], "1.6.4")

    def test_create_action(self):
        self.assertEqual(self.result["resource_changes"][0]["change"]["actions"], ['create'])

    def test_instance_type(self):
        self.assertEqual(self.runner.get_value("aws_instance.foo", "instance_type"), "t2.micro")

    def test_ami(self):
        self.assertEqual(self.runner.get_value("aws_instance.foo", "ami"), "foo")


class TestE2EModule(unittest.TestCase):
    def setUp(self):
        self.snippet = """
        provider "aws" {
            region  = "eu-west-2"
            access_key = "foo"
            secret_key = "bar"
            skip_credentials_validation = true
            skip_requesting_account_id = true
        }

        module "foo" {
            source = "./mymodule"
        }
        """
        self.runner = Runner(self.snippet)
        self.result = self.runner.result

    def test_root_module(self):
        print(self.result)
        self.assertEqual(self.result["configuration"]["root_module"]["module_calls"]["foo"]["source"], "./mymodule")

    def test_instance_type(self):
        self.assertEqual(self.runner.get_value("module.foo.aws_instance.foo", "instance_type"), "t2.micro")

    def test_ami(self):
        self.assertEqual(self.runner.get_value("module.foo.aws_instance.foo", "ami"), "foo")


if __name__ == '__main__':
    unittest.main()
