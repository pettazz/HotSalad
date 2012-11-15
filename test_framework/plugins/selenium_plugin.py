"""
This is a base selenium plugin, that takes in some of the default parameters
a test will need.  It also provides a webdriver object for the tests to use.
"""

import time
import os

from nose.plugins import Plugin
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from test_framework.core import selenium_launcher
from test_framework.core.locators_manager import LocatorsManager
from test_framework.fixtures.page_interactions import PageInteractions
from test_framework.fixtures.page_loads import PageLoads
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

    def options(self, parser, env):
        super(SeleniumBase, self).options(parser, env=env)
        
        parser.add_option('--browser', action='store',
                          dest='browser',
                          choices=constants.Browser.VERSION.keys(),
                          default=constants.Browser.FIREFOX,
                          help="""The browser to use.Note, if you want to use
                                  chrome, you have to run the chromium driver.
                        http://code.google.com/p/chromium/downloads/list)""")
        parser.add_option('--browser_version', action='store',
                          dest='browser_version',
                          default="latest",
                          help="""The browser version to use. Explicitly select
                          a version number or use "latest". Currently 
                          supported are Firefox: 3.6, 4, 8, Chrome latest,
                          Safari latest, Internet Explorer: 7, 8, 9. If a 
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
            "browserName": options.browser   
        }
        if options.browser == constants.Browser.INTERNET_EXPLORER:
            self.browser_settings["platform"] = "WINDOWS"
            self.browser_settings["browserName"] = "internet explorer"
        
        if options.browser_version == 'latest':
            version = constants.Browser.LATEST[options.browser]
            if version is not None:
                self.browser_settings["version"] = version
        else:
            version_options = constants.Browser.VERSION[options.browser]
            if (version_options is not None and 
                options.browser_version in version_options):
                self.browser_settings["version"] = options.browser_version
                
        self.options = options

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
                    print "Attempt #%s to connect to Selenium failed" % i
                    if i < 3:
                        print "Retrying in 15 seconds..."
                        time.sleep(15)
            if not connected:
                print "Error starting/connecting to Selenium:"
                print err
                print "\n\n\n"
                os.kill(os.getpid(), 9)

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
