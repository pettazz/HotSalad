import getpass
import time
import unittest

from mock.mock_objects import *

from test_framework.core.testcase_manager import ExecutionQueryPayload
from test_framework.core.testcase_manager import TestcaseDataPayload
from test_framework.plugins import db_reporting_plugin

class DBReportingTestCase(unittest.TestCase):
    def setUp(self):
        self.execution_db = ExecutionQueryPayload().get_params()
        self.testcase_db = TestcaseDataPayload().get_params()
        db_reporting_plugin.TestcaseManager = MockTestcaseManager
        db_reporting_plugin.TestcaseManager.execution_db = self.execution_db
        db_reporting_plugin.TestcaseManager.testcase_db = self.testcase_db
        self.plugin = db_reporting_plugin.DBReporting()
        self.plugin.options = MockOptions()
        self.plugin.testcase_manager = MockTestcaseManager()

    def test_begin(self):
        self.test = MockTestSuite()
        self.plugin.begin()
        db = self.execution_db
        self.assertTrue(db['guid'] == MockTestcaseManager().mock_execution_guid)
        self.assertTrue(db['username'] == getpass.getuser())
        self.assertTrue(db['execution_start_time'] <= int(time.time() * 1000))
    
    def test_start_test(self):
        self.test = MockTest()
        self.plugin.begin()
        self.plugin.startTest(self.test)
        db = self.testcase_db
        self.assertTrue(db['state'] == "NotRun")
        self.assertTrue(db['application'] == "nosetests.nose.1234abcd")
        self.assertTrue(db['testcaseAddress'] == "test")
        self.assertTrue(db['browser'] == "Silk-browser")
        self.assertTrue(self.plugin.case_start_time <= int(time.time() * 1000))

    def test_add_success(self):
        self.test = MockTest()
        self.plugin.begin()
        self.plugin.addSuccess(self.test, "wat")
        db = self.testcase_db
        self.assertTrue(db['state'] == "Pass")

    def test_add_error(self):
        self.test = MockTest()
        self.plugin.begin()
        self.plugin.addError(self.test, "Stuff got broke")
        db = self.testcase_db
        self.assertTrue(db['state'] == "Error")

    def test_add_failure(self):
        self.test = MockTest()
        self.plugin.begin()
        self.plugin.addFailure(self.test, "Stuff did not pass")
        db = self.testcase_db
        self.assertTrue(db['state'] == "Fail")

    def test_finalize(self):
        self.result = MockResult()
        self.plugin.begin()
        time.sleep(1)
        self.plugin.finalize(self.result)
        db = self.execution_db
        self.assertTrue(db['runtime'] > 0)


if __name__ == '__main__':
    unittest.main()
