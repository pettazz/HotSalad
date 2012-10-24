"""
This class containts constats that are standard through our the test framework
"""
class Environment:
    QA = "qa"
    PRODUCTION = "production"
    LOCAL = "local"

class Browser:
    FIREFOX = "firefox"
    INTERNET_EXPLORER = "ie"
    SAFARI = "safari"
    GOOGLE_CHROME = "chrome"
    HTML_UNIT = "htmlunit"

    VERSION = {
        "firefox" : ["9", "3.6"],
        "ie" : ["8", "9"],
        "chrome" : None,
        "htmlunit" : None
    }

    LATEST = {
        "firefox": "9",
        "ie": "9",
        "chrome": None,
        "htmlunit": None
    }

class State:
    NOTRUN = "NotRun"
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

#define the default s3 upload details
class s3ManagerAccount:
    LOG_BUCKET = "seleniumlogs", 
    BUCKET_URL = "http://myseleniumstuff.s3-website-us-east-1.amazonaws.com/",
    SELENIUM_ACCESS_KEY = "HAHAHAOHWOW",
    SELENIUM_SECRET_KEY = "/hunter2"