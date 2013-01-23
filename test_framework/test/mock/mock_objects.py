"""
This class represents mock objects.  These can be used to unit test code
that requires the existance of these objects without creating real ones.
"""
class MockOptions():
    servername = "localhost"
    port = None
    log_path = "unittest_logs"
    browser = 'Silk-browser'
    browser_version = 'latest'


class MockTestSuite():

    def __init__(self):
        self.test = MockTest()

class MockTest():

    def __init__(self):
        self.app_name = 'nosetests'
        self.unique_id = 1337
        self.app_env = 'qaprod'
        self.user = 'nose'
        self.api_key = '1234abcd'
        self.browser = 'Silk-browser'
        self.driver = MockDriver()
        self.testcase_guid = 'rofltestcase'
        self.execution_guid = 'roflexecution'
        self.sauce_job_id = '8'

    def id(self):
        return "test"

class MockDriver():

    current_url = "http://this_is_a_test.org/wowzers"
    page_source = "source code"

    def get_screenshot_as_file(self, file_name):
        file_obj = open(file_name, "w")
        file_obj.close()

class MockTestcaseManager():

    def __init__(self):
        self.mock_execution_guid = 'roflexecution'
        self.mock_testcase_guid = 'rofltestcase'
    
    def insert_execution_data(self, data_payload):
        self.execution_db.update(data_payload.get_params())
        self.execution_db['guid'] = self.mock_execution_guid
        return self.mock_execution_guid

    def update_execution_data(self, guid, runtime):
        self.execution_db['runtime'] = runtime
        return self.mock_execution_guid

    def insert_testcase_data(self, data_payload):
        self.testcase_db.update(data_payload.get_params())
        self.execution_db['guid'] = self.mock_execution_guid
        return self.mock_execution_guid

    def update_testcase_data(self, data_payload):
        self.testcase_db.update(data_payload.get_params())
        self.execution_db['guid'] = self.mock_execution_guid
        return self.mock_execution_guid

class MockResult:
    nothing = None