"""
This is a base plugin that takes in log path to start
"""

import os
import shutil
import time

from nose.plugins import Plugin
from nose.exc import SkipTest

from test_framework.fixtures import constants, errors


class Base(Plugin):
    """
    The base plugin for selneium tests that includes the
    following variables:
    self.options.log_path -- the directory in which the log files are saved
                              (--log_path)
    """
    name = 'hotsalad_test'

    def options(self, parser, env):
        super(Base, self).options(parser, env=env)
        parser.add_option('--log_path', dest='log_path',
                          default='logs/',
                          help='Where the log files are saved')
        
    def configure(self, options, conf): 
        super(Base, self).configure(options, conf) 
        if not self.enabled:
            return
        self.options = options
        if options.log_path.endswith("/"):
            options.log_path = options.log_path[:-1]
        if not os.path.exists(options.log_path):
            os.mkdir(options.log_path)
        else:
            if not os.path.exists("%s/../archived_logs/" % options.log_path):
                os.mkdir("%s/../archived_logs/" % options.log_path)
            shutil.move(options.log_path, "%s/../archived_logs/logs_%s"%(
                        options.log_path, int(time.time())))
            os.mkdir(options.log_path)

            
    def beforeTest(self, test):
        test_logpath = self.options.log_path + "/" + test.id()
        if not os.path.exists(test_logpath):
            os.mkdir(test_logpath)

        #set test scope options variables here. ex:
        #test.test.some_id_thing = self.options.some_id_thing

    
    def addError(self, test, err, capt=None):
        """
        Since Skip, Blocked, and Deprecated are all technically errors, but not
        error states, we want to make sure that they don't show up in nose output
        as errors.
        """
        if (err[0] == errors.BlockedTest or 
            err[0] == errors.SkipTest or
            err[0] == errors.DeprecatedTest):
            print err[1].__str__().split('-------------------- >> begin captured logging << --------------------', 1)[0]

    def handleError(self, test, err, capt=None):
        """
        If the database plugin is not present, we have to handle capturing
        "errors" that shouldn't be reported as such in base.
        """
        if not hasattr(test.test, "testcase_guid"):
            if err[0] == errors.BlockedTest:
                raise SkipTest(err[1])
                return True
                
            elif err[0] == errors.DeprecatedTest:
                raise SkipTest(err[1])
                return True
                
            elif err[0] == errors.SkipTest:
                raise SkipTest(err[1])
                return True