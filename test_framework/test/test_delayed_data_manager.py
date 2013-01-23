import datetime
import time
import unittest
import uuid

from test_framework.core.delayed_data_manager import DelayedTestStorage, DelayedTestAssistant

class UnitTests(unittest.TestCase):

    def test_add_row_delayedTestData(self):
        """Test that data can be inserted into and extracted from delayedTestData"""
        generated_uuid = str(uuid.uuid4())
        timestamp = datetime.datetime.fromtimestamp(time.time()).isoformat()
        expected_result = "test_of_delayed_test+%s" % timestamp
        test_id = "DelayedUnitTestAddRow"
        DelayedTestStorage.insert_delayed_test_data(generated_uuid, test_id, expected_result, 0, 1000000000000)
        # Now check that we can pull the data out
        data = DelayedTestStorage.get_delayed_test_data(testcase_address=test_id)
        extracted_uuid = None
        self.assertTrue(data is not None)
        for item in data:
            if ((item[3] == expected_result)):
                extracted_uuid = item[0]
                break
        self.assertEqual(generated_uuid, extracted_uuid)
        # Check that we can change the data
        DelayedTestStorage.set_delayed_test_to_done(generated_uuid)
        data = DelayedTestStorage.get_delayed_test_data(testcase_address=test_id, done=1)
        self.assertTrue(data is not None)
        for item in data:
            if (item[0] == generated_uuid):
                self.assertEqual(item[4], 1)
                break
        DelayedTestAssistant.get_delayed_results(test_id=test_id, seconds=1, set_done=True) # Clean Up

    def test_get_data_from_delayedTestData_set_done_later(self):
        """Test that data can be extracted from delayedTestData without making it done until later"""
        generated_uuid = str(uuid.uuid4())
        timestamp = datetime.datetime.fromtimestamp(time.time()).isoformat()
        expected_result = "test_of_delayed_test+%s" % timestamp
        test_id = "DelayedUnitTestSetDoneLater"
        # First clear any leftover rows from previous unittests of this
        DelayedTestAssistant.get_delayed_results(test_id=test_id, seconds=1, set_done=True)
        # Now begin putting in new data
        DelayedTestStorage.insert_delayed_test_data(generated_uuid, test_id, expected_result, 0, 1000000000000)
        time.sleep(1.2)
        for item in DelayedTestAssistant.get_delayed_results(test_id=test_id, seconds=1, set_done=False):
            pass # making sure data was not set to done (if not working, no data would come later)
        found = False
        for item in DelayedTestAssistant.get_delayed_results(test_id=test_id, seconds=1, set_done=False):
            found = True
            extracted_guid = item[0]
            self.assertEqual(extracted_guid, generated_uuid)
            DelayedTestAssistant.set_test_done(extracted_guid)
        self.assertTrue(found)
        found = False
        for item in DelayedTestAssistant.get_delayed_results(test_id=test_id, seconds=1, set_done=False):
            found = True
        self.assertFalse(found) # Should not find anything this time
        DelayedTestAssistant.get_delayed_results(test_id=test_id, seconds=1, set_done=True) # Clean Up
