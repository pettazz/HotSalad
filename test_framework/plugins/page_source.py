"""
contains the plugin for capturing and storing source code
on errors and failures
"""

import codecs

from nose.plugins import Plugin

class PageSource(Plugin):
    """
    This plugin will capture source code when a test raises an error
    or when a test fails. It will store that sourcecode either in
    the default logs file or another file of the user's specification,
    along with default test and time ran info.
    """

    name = "page_source"
    logfile_name = "page_source.html"
    
    def options(self, parser, env):
        super(PageSource, self).options(parser, env=env)

    def configure(self, options, conf):
        super(PageSource, self).configure(options, conf)
        if not self.enabled:
            return
        self.options = options
        
    def addError(self, test, err,capt=None):
        test_logpath = self.options.log_path + "/" + test.id()
        html_file_name = "%s/%s" % (test_logpath, self.logfile_name)
        html_file = codecs.open(html_file_name, "w","utf-8")
        html_file.write(test.driver.page_source)
        html_file.close()
        
    def addFailure(self, test, err, capt=None,tbinfo = None):
        test_logpath = self.options.log_path + "/" + test.id()
        html_file_name = "%s/%s"%(test_logpath,self.logfile_name)
        html_file = codecs.open(html_file_name, "w","utf-8")
        html_file.write(test.driver.page_source)
        html_file.close()

        
        
