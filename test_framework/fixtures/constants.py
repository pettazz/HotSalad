"""
This class containts constats that are standard through our the test framework
"""
class Environment:
    QA = "qa"
    PRODUCTION = "production"
    LOCAL = "local"
    STAGING = "staging"

class Sauce:
    USER = 'sauce_user'
    ACCESS_KEY = 'some-key-stuff'

class Browser:
    FIREFOX = "firefox"
    INTERNET_EXPLORER = "ie"
    SAFARI = "safari"
    GOOGLE_CHROME = "chrome"
    IPAD = "iPad"
    HTML_UNIT = "htmlunit"

    VERSION = {
        "firefox" : ["16"],
        "ie" : ["8", "9"],
        "safari": ["6"],
        "chrome" : ["23"],
        "iPad" : ["5.1", "6"],
        "htmlunit" : None
    }

    LATEST = {
        "firefox": "16",
        "ie": "9",
        "safari": "6",
        "chrome": "23",
        "iPad": "6",
        "htmlunit": None
    }

class State:
    NOTRUN = "Incomplete"
    ERROR = "Error"
    FAILURE = "Fail"
    PASS = "Pass"
    SKIP = "Skip"
    BLOCKED = "Blocked"
    DEPRECATED = "Deprecated"

#define the default account to log into with the EmailManager fixture
class EmailManagerAccount:
    USERNAME = 'dudebro99@gmail.com'
    PASSWORD = 'hunter2'

#define default log file upload location
class LogUploader:
    USE_S3 = False
    #settings defined in constants.s3ManagerAccount

    USE_LOCAL = True
    DESTINATION_PATH = '/var/www/'
    BASE_URL = 'http://localhost/'

    #USE_SSH = False
    #fabric?
#define the default s3 upload details
class s3ManagerAccount:
    LOG_BUCKET = "seleniumlogs", 
    BUCKET_URL = "http://myseleniumstuff.s3-website-us-east-1.amazonaws.com/",
    SELENIUM_ACCESS_KEY = "HAHAHAOHWOW",
    SELENIUM_SECRET_KEY = "/hunter2"