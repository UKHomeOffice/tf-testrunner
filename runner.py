# go get github.com/wybczu/tfjson
import json
import os
import sys
import shutil
import subprocess
import tempfile
import glob
from tf_assertion_helper import finder

class Runner(object):
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
        fh = open("%s/mytf.tf" % (self.tmpdir), "w")
        fh.write(self.snippet)
        fh.close()

    def _teraform_plan(self):
        os.system("terraform plan -input=false -out=%s/mytf.tfplan %s" % (self.tmpdir, self.tmpdir))

    def _copy_tf_files(self):
        os.system("rm -rf .terraform/modules")
        os.system("mkdir %s/mymodule" % self.tmpdir)

        files = glob.iglob(os.path.join(sys.path[0], "*.tf"))
        for file in files:
            if os.path.isfile(file):
                shutil.copy(file, "%s/mymodule" % (self.tmpdir))

    def run(self):
        self._mktmpdir()
        self._write_test_tf()
        self._copy_tf_files()
        self._terraform_init()
        self._teraform_plan()
        json = self.snippet_to_json()
        result = self.json_to_dict(json)
        self.result = result
        self._removetmpdir()

    def snippet_to_json(self):
        return subprocess.check_output(["tfjson", "%s/mytf.tfplan" % (self.tmpdir)])

    @staticmethod
    def json_to_dict(json_file):
        return json.loads(json_file)

    def finder(parent, starts_with, matching_object):
        return finder(parent, starts_with, matching_object)