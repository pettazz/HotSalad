# import unittest
# import time
# import os
# from selenium import webdriver

# from test_framework.core import selenium_launcher
# from mock.mock_objects import MockTestSuite

    
# class TestRunV2Jar(unittest.TestCase):

#     def test_selenium_launcher(self):

#         test = MockTestSuite()
#         test.test.server = "localhost"
#         test.test.port = "4444"
#         test.test.log_path = "unittest_logs"
#         os.makedirs("unittest_logs/")
#         selenium_launcher.execute_selenium(test.test.server, test.test.port,
#                                            test.test.log_path)
#         time.sleep(10)
#         try:
#             driver = webdriver.Remote("http://%s:%s/wd/hub"%
#                                       (test.test.server, test.test.port),
#                                       webdriver.DesiredCapabilities.FIREFOX)
#             driver.quit()
#         except:
#             raise Exception ("Selenium did not load.")


#     def tearDown(self):
#         os.remove("unittest_logs/log_seleniumOutput.txt")
#         os.remove("unittest_logs/log_seleniumError.txt")
#         os.removedirs("unittest_logs")

                                    
        
#### This won't work unless we have a grid to connect to