import time
import sys

if sys.version_info >= (2,7):
   # unittest2 features are native in Python 2.7
   import unittest
else:
   import unittest2 as unittest

from test_framework.fixtures import constants,page_loads,page_interactions
#all these can be imported with only one line instead:
#from test_framework.fixtures import tools
from test_framework.fixtures import errors

class ExampleTests(unittest.TestCase):
    app_name = "Example Test"

    def setUp(self):
        """
        Perform basic tasks that need to be done before each test is run.
        """
        self.url = "http://google.com"

    def test_application_load(self):
        """
        This test shows an ideal why to do an application load.
        """
        self.driver.get('http://google.com')

    def test_load_page_verify_element(self):
        """
        This test shows the best way to load a page.  We want to be able to
        verify that we are on the right page, and that important elements have
        loaded.
        """
        self.driver.get(self.url)
        page_loads.wait_for_element_visible(self.driver, "img.hplogo")
        

    def test_skip_test_on_condition(self):
        """
        Some tests will need certain conditions to be met in order to run 
        that are outside the scope of the test itself. If the conditions aren't
        right, we can skip the test.
        """
        self.driver.get(self.url)
        #for some reason this element's presence means we can't run our test
        if page_interactions.is_element_present(self.driver, "body"):
            raise errors.SkipTest("The body is here so I can't run.")

    def test_blocked_test(self):
        """
        If a test is blocked by an issue in Jira for example, we can rais a 
        BlockedTest exception to record this.
        """
        raise errors.BlockedTest("This test is blocked by JIRA EXAMPLE-218")

        self.driver.get(self.url)

    def test_deprecated(self):
        """
        When a test becomes deprecated, it can be marked as such, preventing
        it from being run and recording it a such, until it's removed.
        """
        raise errors.DeprecatedTest(
            "This test will be replaced by test_example2 when app is ready.")
        
        self.driver.get(self.url)