"""
This file contains database credentials for the various databases the tests
need to access
"""
# Environments
QA = "qa"
LOCAL = "local"
PROD = "prod"
TEST = "test"

class Apps:
    TESTCASE_REPOSITORY = "testcase_repository"


APP_CREDS = {
    Apps.TESTCASE_REPOSITORY: {
        PROD: ("127.0.0.1", 
               "root", "", "TestcaseData"),
        QA: ("127.0.0.1", 
             "root", "", "TestcaseData")
    },

}