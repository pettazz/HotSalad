"""
This is a base selenium plugin, that takes in some of the default parameters
a test will need.  It also provides a webdriver object for the tests to use.
"""

import time
import os, sys
import traceback, codecs

from nose.plugins import Plugin
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from test_framework.core import selenium_launcher
from test_framework.core.locators_manager import LocatorsManager
from test_framework.core.page_interactions import PageInteractions
from test_framework.core.page_loads import PageLoads
from test_framework.fixtures import constants


class SeleniumBase(Plugin):
    """
    The base plugin for selneium tests. Takes in  key arguments, and then
    creates a webdriver object.  Passes all those arguments to the tests.

    The following variables are made to the tests:
    self.options.browser -- the browser to use (--browser)
    self.options.server -- the server used by the test (--server)
    self.options.port -- the port used by thest (--port)

    """
    name = 'selenium'
    
    # sources to use in logging for errors and failures
    log_sources = ['validation_pane', 'javascript_console']

    def options(self, parser, env):
        super(SeleniumBase, self).options(parser, env=env)
        
        parser.add_option('--browser', action='store',
                          dest='browser',
                          choices=constants.Browser.VERSION.keys(),
                          default=constants.Browser.FIREFOX,
                          help="""The browser to use.Note, if you want to use
                                  Chrome, you have to install the chromedriver.
                        http://code.google.com/p/chromium/downloads/list)""")
        parser.add_option('--browser_version', action='store',
                          dest='browser_version',
                          default="latest",
                          help="""The browser version to use. Explicitly select
                          a version number or use "latest". Currently 
                          supported are Firefox latest, Chrome latest, and
                          Internet Explorer 8 and 9. If a 
                          version is not specified, one will be selected from 
                          the currently available servers.""")
        parser.add_option('--server', action='store', dest='servername',
                          default='localhost',
                          help="designates the server used by the test")
        parser.add_option('--port', action='store', dest='port',
                          default='4444',
                          help="designates the port used by the test")

    def configure(self, options, conf):
        super(SeleniumBase, self).configure(options, conf)
        if not self.enabled:
            return

        #determine the browser version to use and create our own 
        #DesiredCapabilities dict
        self.browser_settings = {
            "browserName": options.browser,
            "selenium-version": '2.28.0'
        }
        
        if options.browser_version == 'latest':
            version = constants.Browser.LATEST[options.browser]
            if version is not None:
                self.browser_settings["version"] = version
        else:
            version_options = constants.Browser.VERSION[options.browser]
            if (version_options is not None and 
                options.browser_version in version_options):
                self.browser_settings["version"] = options.browser_version

        # browser-specific capabilities settings:
        # ie
        if options.browser == constants.Browser.INTERNET_EXPLORER:
            if options.browser_version == 'latest' or options.browser_version == '9':
                self.browser_settings["platform"] = "Windows 2008"
            else:
                self.browser_settings["platform"] = "WINDOWS"
            self.browser_settings["browserName"] = "internet explorer"

        # ipad
        if options.browser == constants.Browser.IPAD:
            self.browser_settings["platform"] = 'Mac 10.8'
                
        self.options = options

        # chrome
        #  kind of a hack for sauce 
        if options.browser == constants.Browser.GOOGLE_CHROME:
            self.browser_settings["version"] = ''


        if (self.options.servername == "localhost" and
            self.options.browser == constants.Browser.HTML_UNIT):
            selenium_launcher.execute_selenium(self.options.servername,
                                               self.options.port,
                                               self.options.log_path)
            time.sleep(20)
            try:
                driver = webdriver.Remote("http://%s:%s/wd/hub" %
                                          (self.options.servername,
                                          self.options.port),
                                          DesiredCapabilities.HTML_UNIT)
                driver.quit()
            except:
                raise Exception ("Selenium did not launch. Try again.")

    def beforeTest(self, test):
        """ Running Selenium locally will be handled differently
            from how Jenkins runs Selenium remotely.
            More changes may be needed in the future. """
        self.browser_settings['name'] = test.test.id()
        self.browser_settings['custom-data'] = {
            'execution_guid': test.test.execution_guid,
            'testcase_guid': test.test.testcase_guid
        }

        if self.options.servername == "localhost":
            try:
                self.driver = self.__select_browser(self.options.browser)
                test.test.driver = self.driver
                if "version" in self.browser_settings.keys():
                    version = self.browser_settings["version"]
                else:
                    version = ""
                test.test.browser = "%s%s" % (self.options.browser, version)
            except Exception as err:
                print "Error starting/connecting to Selenium:"
                print err
                os.kill(os.getpid(), 9)
        else:
            connected = False
            for i in range(1, 4):
                try:
                    self.driver = self.__select_browser(self.options.browser)
                    test.test.driver = self.driver
                    if "version" in self.browser_settings.keys():
                        version = self.browser_settings["version"]
                    else:
                        version = ""
                    test.test.browser = "%s%s" % (self.options.browser, version)
                    connected = True
                    break
                except Exception as err:
                    #nose swallows beforeTest exceptions, so this is the only way
                    #to get the word out when stuff breaks here.
                    print err
                    print "Attempt #%s to connect to Selenium failed" % i
                    if i < 3:
                        print "Retrying in 15 seconds..."
                        time.sleep(15)
            if not connected:
                print "Error starting/connecting to Selenium:"
                print err
                print "\n\n\n"
                os.kill(os.getpid(), 9)

        # sauce hax
        if not self.options.browser in (constants.Browser.INTERNET_EXPLORER, constants.Browser.GOOGLE_CHROME):
            self.driver.maximize_window()

        # get sauce id if we're using it
        if(hasattr(self.driver, 'session_id') and '-' not in self.driver.session_id):
            # checking for - is so janky but it works
            test.test.sauce_job_id = self.driver.session_id
        else:
            test.test.sauce_job_id = None

        # also set up the selenium helper instances
        # locators helper
        if(hasattr(test.test, 'locators')):
            locators = test.test.locators
        else:
            locators = None
        test.test.locators = LocatorsManager(self.driver, locators)

        # page_loads helper
        test.test.page_loads = PageLoads(self.driver)

        # page_interactions helper
        test.test.page_interactions = PageInteractions(self.driver)


    def afterTest(self, test):
        try:
            self.driver.quit()
        except:
            print "No driver to quit."

    def addError(self, test, err, capt=None):
        self.__gather_errors(test)

    def addFailure(self, test, err, capt=None, tbinfo=None):
        self.__gather_errors(test)

    def __gather_errors(self, test):
        gathered_logs = {}

        # get the logs
        for source in self.log_sources:
            try:
                gathered_logs[source] = getattr(self, source + "_gather")(test)
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                gathered_logs[source] = [
                    "Logging could not be retrieved for this source.", 
                    "Traceback: " + ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
                ]

        # write all the log files
        for log_type in gathered_logs:
            logfile_name = log_type + ".log"
            test_logpath = self.options.log_path + "/" + test.id()
            file_name = "%s/%s" % (test_logpath, logfile_name)
            file_handle = codecs.open(file_name, "w", "utf-8")
            file_handle.writelines("\r\n".join(gathered_logs[log_type]))
            file_handle.close()

    def javascript_console_gather(self, test):
        return ["Not implemented yet."]

    # example of a log gathering method
    # def example_data_gather(self, test):
    #     return test.some_helper.get_validation_error_messages()

    def __select_browser(self, browser_name):
        if (self.options.servername != "localhost" or
            self.options.browser == constants.Browser.HTML_UNIT):
            return webdriver.Remote("http://%s:%s/wd/hub" %
                                    (self.options.servername,
                                    self.options.port),
                                    self.browser_settings)
        else:
            if browser_name == constants.Browser.FIREFOX:
                return webdriver.Firefox()
            if browser_name == constants.Browser.INTERNET_EXPLORER:
                return webdriver.Ie()
            if browser_name == constants.Browser.GOOGLE_CHROME:
                return webdriver.Chrome()
            if browser_name == constants.Browser.SAFARI:
                return webdriver.Safari()
            else:
                print "No recognized browser was selected!"
                raise Exception("No recognized browser was selected!")
