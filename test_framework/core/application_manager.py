"""

Methods for generating and parsing application strings used 
in the Testcase Database

"""
class ApplicationManager:
    """
    This class contains methods to generate application strings.  We build
    it from available test data
    """
    @classmethod
    def generate_application_string(cls, test):
        """generate an application string based on any of the given information
           that can be pulled from the test object: app_name, user, api_key"""
        
        app_name = ''
        user = ''
        api_key = ''
        
        if hasattr(test, 'app_name'):
            app_name = test.app_name

        if hasattr(test, 'user'):
            user = test.user

        if hasattr(test, 'api_key'):
            api_key = test.api_key

        return "%s.%s.%s" % (app_name, user, api_key)
        
    @classmethod
    def parse_application_string(cls, string):
        """parse a generated application string into its parts:
            app_name, user, api_key"""
        
        pieces = string.split('.')
        return pieces[0], pieces[1], pieces[2], 