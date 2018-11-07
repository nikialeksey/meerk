# MIT License
#
# Copyright (c) 2018 Alexey Nikitin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from unittest import TestCase

import pycodestyle
from pylint import epylint as lint
import mypy.api


class StaticAnalysisTest(TestCase):

    def test_style(self):
        result = self.__pycodestyle('./meerk/')
        self.assertEqual(result.total_errors, 0, "Found code style errors or warnings.")

    def test_style_tests(self):
        result = self.__pycodestyle('./tests/')
        self.assertEqual(result.total_errors, 0, "Found tests style errors or warnings.")

    def test_code_lint(self):
        self.__pylint('./meerk')

    def test_tests_lint(self):
        self.__pylint('./tests')

    def test_code_mypy(self):
        self.__mypy('./meerk')

    def test_tests_mypy(self):
        self.__mypy('./tests')

    def __mypy(self, path: str):
        (out, err, code) = mypy.api.run([path, '--config-file=./tests/mypy.ini'])
        if err:
            self.fail(err)
        if code != 0:
            self.fail(out)

    def __pycodestyle(self, path: str):
        # pylint: disable=R0201
        style = pycodestyle.StyleGuide(config_file='./tests/pycodestyle.ini')
        return style.check_files([path])

    def __pylint(self, path: str):
        (out, err) = lint.py_run(path + ' --rcfile=./tests/pylint.ini', return_std=True)
        errors = err.read()  # type: str
        report = out.read()  # type: str
        if errors:
            self.fail(errors)
        elif 'Your code has been rated at 10.00/10' not in report:
            self.fail(report)
