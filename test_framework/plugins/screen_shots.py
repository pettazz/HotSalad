"""
Contains the plugin for screenshots for the selenium tests.
"""

from nose.plugins import Plugin


class ScreenShots(Plugin):
    """
    This plugin will take a screenshot when a test raises an error
    or when a test fails. It will store that screenshot either in
    the default logs file or another file of the user's specification
    along with default test and time ran info.
    """
    
    name = "screen_shots"

    logfile_name = "screenshot.jpg"

    def options(self, parser, env):
        super(ScreenShots, self).options(parser, env=env)
        
    def configure(self, options, conf):
        super(ScreenShots, self).configure(options, conf)
        if not self.enabled:
            return
        self.options = options
        
    def addError(self, test, err, capt=None):
        test_logpath = self.options.log_path + "/" + test.id()
        screenshot_file = "%s/%s" % (test_logpath, self.logfile_name)
        test.driver.get_screenshot_as_file(screenshot_file)
        
    def addFailure(self, test, err, capt=None, tbinfo=None):
        test_logpath = self.options.log_path + "/" + test.id()
        screenshot_file = "%s/%s" % (test_logpath, self.logfile_name)
        test.driver.get_screenshot_as_file(screenshot_file)

