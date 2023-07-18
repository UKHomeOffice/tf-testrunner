# go get github.com/wybczu/tfjson
# pylint: disable=missing-docstring, E0213, W0201
import json
import os
import sys
import shutil
import subprocess
import tempfile
import glob
from tf_assertion_helper import finder, get_value


class Runner:
    """Terraform converter, converting .tf files into JSON and Python"""

    def __init__(self, snippet):
        self.snippet = snippet
        self.run()

    def _removetmpdir(self):
        shutil.rmtree(self.tmpdir)

    def _mktmpdir(self):
        self.tmpdir = tempfile.mkdtemp()

    def _terraform_init(self):
        subprocess.call(["terraform", "init", self.tmpdir])

    def _write_test_tf(self):
        with open(f"{self.tmpdir}/mytf.tf", "w", encoding="utf-8") as tmp_mytf_file:
            tmp_mytf_file.write(self.snippet)

    def _terraform_plan(self):
        os.system(f"terraform plan -input=false -out={self.tmpdir}/mytf.tfplan {self.tmpdir}")

    def _copy_tf_files(self):
        os.system("rm -rf .terraform/modules")
        os.system(f"mkdir {self.tmpdir}/mymodule")

        files = glob.iglob(os.path.join(sys.path[0], "*.tf"))
        for file in files:
            if os.path.isfile(file):
                shutil.copy(file, f"{self.tmpdir}%s/mymodule")

    def run(self):
        self._mktmpdir()
        self._write_test_tf()
        self._copy_tf_files()
        self._terraform_init()
        self._terraform_plan()
        json_snippet = self.snippet_to_json()
        result = self.json_to_dict(json_snippet)
        self.result = result
        self._removetmpdir()

    def snippet_to_json(self):
        return subprocess.check_output(["terraform", "show", "-no-color", "-json",
                                        f"{self.tmpdir}/mytf.tfplan"])

    def get_value(self, match_address, match_value):
        return get_value(self.result, match_address, match_value)

    @staticmethod
    def json_to_dict(json_file):
        return json.loads(json_file)

    def finder(parent, starts_with, matching_object):
        return finder(parent, starts_with, matching_object)
