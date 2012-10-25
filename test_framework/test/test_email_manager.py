# import unittest

# from BeautifulSoup import BeautifulSoup
# from test_framework.fixtures.email_manager import EmailException
# from test_framework.fixtures.email_manager import EmailManager

# class UnitTests(unittest.TestCase):

#     def test_search_for_email_by_subject(self): # uses the default imap connection settings
#         """ Test that you can search for an email by subject """
#         email_manager = EmailManager("selenese.ateam@gmail.com")
#         result = email_manager.search(SUBJECT="Sub-999unittest",
#                                       content_type="PLAIN", timeout=15)
#         text = BeautifulSoup(result.items()[0][1])
#         self.assertTrue("This is a test of the magic number 999." in str(text))


#     def test_search_for_email_by_recipient(self): # uses the default imap connection settings
#         """ Test that you can search for an email by recipient """
#         email_manager = EmailManager("selenese.ateam@gmail.com")
#         result = email_manager.search(TO="selenese.ateam+999888unittest@gmail.com",
#                                       content_type="HTML", timeout=15)
#         text = BeautifulSoup(result.items()[0][1])
#         self.assertTrue("Your base is under attack! Unittest!" in str(text))


#     def test_search_for_email_not_exist(self): # uses the default imap connection settings
#         """ Test that you raise an exception when searching for a non-existing email """
#         email_manager = EmailManager("selenese.ateam@gmail.com")
#         try:
#             result = email_manager.search(SUBJECT="This email doesn't exist - exception unittest",
#                                           content_type="PLAIN", timeout=15)
#             raise Exception("Expected Exception not raised")
#         except EmailException:
#             pass # This should get thrown when the email is not found


#     def test_remove_whitespace(self):
#         """ Test that remove_whitespace works """
#         email_manager = EmailManager("selenese.ateam@gmail.com")
#         text = "\tHere is a random line\r\n"
#         self.assertEquals(email_manager.remove_whitespace(text), "Here is a random line")


#### I'm too lazy to set up a real gmail just to test this