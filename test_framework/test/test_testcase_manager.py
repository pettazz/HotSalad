import getpass
import math
import time
import unittest

from test_framework.core.mysql import DatabaseManager
from test_framework.core.testcase_manager import ExecutionQueryPayload
from test_framework.core.testcase_manager import TestcaseDataPayload
from test_framework.core.testcase_manager import TestcaseManager as TCM

class TestTestcaseManager(unittest.TestCase):
	
    def setUp(self):
        self.manager = TCM('qa')

    def tearDown(self):
        query = """DELETE FROM execution WHERE guid = %(guid)s"""
        DatabaseManager('qa').execute_query_and_close(query,
                                                  {"guid":"anexecutionguid"})

        query = """DELETE FROM testcaseRunData WHERE guid = %(guid)s"""
        DatabaseManager('qa').execute_query_and_close(query,
                                                  {"guid":'antestcaseguid'})

    def test_insert_execution_data(self):
        payload = ExecutionQueryPayload()
        payload.guid = "anexecutionguid"
        payload.execution_start_time = 1234567890
        payload.username = "myself"
        self.manager.insert_execution_data(payload)

        query = """SELECT * FROM execution WHERE guid = %(guid)s"""
        results = DatabaseManager('qa').fetchone_query_and_close(query, {"guid":'anexecutionguid'})

        self.assertTrue(results[0] == 'anexecutionguid')
        self.assertTrue(results[1] == -1)
        self.assertTrue(results[2] == 'myself')
        self.assertTrue(results[3] == 1234567890)
	
    def test_update_execution_data(self):
        payload = ExecutionQueryPayload()
        payload.guid = "anexecutionguid"
        payload.execution_start_time = 1234
        payload.username = "myself"
        self.manager.insert_execution_data(payload)
        self.manager.update_execution_data("anexecutionguid", 60)

        query = """SELECT * FROM execution WHERE guid = %(guid)s"""
        results = DatabaseManager('qa').fetchone_query_and_close(query, {"guid":'anexecutionguid'})

        self.assertTrue(results[0] == 'anexecutionguid')
        self.assertTrue(results[1] == 60)
        self.assertTrue(results[2] == 'myself')
        self.assertTrue(results[3] == 1234)

    def test_insert_test_case_data(self):
        payload = TestcaseDataPayload()
        payload.guid = "antestcaseguid"
        payload.testcaseAddress = self.id()
        payload.application = "python unittest"
        payload.execution_guid = "executionmachine"
        payload.runtime = 55
        payload.state = "Massachusetts"
        payload.browser = "SeaMonkey"
        self.manager.insert_testcase_data(payload)

        query = """SELECT * FROM testcaseRunData WHERE guid = %(guid)s"""
        results = DatabaseManager('qa').\
            fetchone_query_and_close(query, {"guid":'antestcaseguid'})

        self.assertTrue(results[0] == 'antestcaseguid')
        self.assertTrue(results[1] == self.id())
        self.assertTrue(results[2] == "python unittest")
        self.assertTrue(results[3] == "executionmachine")
        self.assertTrue(results[4] == 55)
        self.assertTrue(results[5] == 'Massachusetts')
        self.assertTrue(results[6] == 'SeaMonkey')
		
    def test_update_test_case_data(self):
        payload = TestcaseDataPayload()
        payload.guid = "antestcaseguid"
        payload.testcaseAddress = self.id()
        payload.application = "python unittest"
        payload.execution_guid = "executionmachine"
        payload.runtime = 55
        payload.state = "Massachusetts"
        payload.browser = "SeaMonkey"
        self.manager.insert_testcase_data(payload)

        new_payload = TestcaseDataPayload()
        new_payload.runtime = 300
        new_payload.state = "Ohio"
        new_payload.retry_count = 82
        new_payload.guid = "antestcaseguid"
        self.manager.update_testcase_data(new_payload)

        query = """
                        SELECT * FROM testcaseRunData WHERE guid = %(guid)s
                """
        results = DatabaseManager('qa').\
            fetchone_query_and_close(query, {"guid":'antestcaseguid'})

        self.assertTrue(results[0] == 'antestcaseguid')
        self.assertTrue(results[1] == self.id())
        self.assertTrue(results[2] == "python unittest")
        self.assertTrue(results[3] == "executionmachine")
        self.assertTrue(results[4] == 300)
        self.assertTrue(results[5] == 'Ohio')
        self.assertTrue(results[6] == 'SeaMonkey')
        self.assertTrue(results[8] == 82)
