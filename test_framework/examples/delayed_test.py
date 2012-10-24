import unittest
import datetime
import json
import uuid
from test_framework.fixtures import page_loads
from test_framework.fixtures.delayed_data_manager import DelayedTestAssistant, DelayedTestStorage
from test_framework.fixtures.email_manager import EmailManager, EmailException


class DelayedTests(unittest.TestCase):

    def setUp(self):
        self.test_id = "%s"%(uuid.uuid4())


    def tearDown(self):
        """
        Clean up any rows we added in the example so that we don't have expiration
        warnings about example data.
        """
        # Example Test ONLY - set the data to done
        if "test_delayed_framework" in str(self.test_id):
            import time; time.sleep(1.2)
            for item in DelayedTestAssistant.get_delayed_results(self.test_id, seconds=1):
                pass  # data will automatically be set to done without using it
        else:
            self.fail("Do not copy/paste this last section into your test!")


    def test_delayed_framework(self):
        """
        This test checks the delayed testing framework by using dummy data.
        """
        result = {}
        # First get all valid data
        for item in DelayedTestAssistant.get_delayed_results(self.test_id, seconds=10):
            extracted_guid = item[0]
            dummy_variable = json.JSONDecoder().decode(item[3])['dummy_variable']

            # Now check the eligible data
            if dummy_variable == "dummy_value":
                result[extracted_guid] = True
            else:
                result[extracted_guid] = False

        # Actual test work is done after the delayed test work
        new_dummy_variable = "dummy_value"

        # Store the data to search for later
        DelayedTestAssistant.store_delayed_data(self.test_id, {'dummy_variable' : new_dummy_variable})

        # Validations
        failed_guids = {}
        for row_guid in result.keys():
            if not result[row_guid]:
                failed_guids[row_guid] = "Failure to see dummy_variable set to dummy_value!"
        self.assertFalse(failed_guids, "Failure rows = %s"%failed_guids)

