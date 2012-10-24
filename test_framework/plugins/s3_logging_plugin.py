"""

S3 Logging plugin to upload all logs to the S3 bucket.

"""

import uuid
import logging
import os

from test_framework.core.s3_manager import S3LoggingBucket
from nose.plugins import Plugin


class S3Logging(Plugin):
    """
    The plugin for uploading test logs to the s3 bucket.
    """
    name = 's3_logging'

    #Plugin methods
    def configure(self, options, conf):
        """get the options"""
        super(S3Logging, self).configure(options, conf)
        self.options = options

    def afterTest(self, test):
        """after each testcase, upload its logs to the S3 bucket"""
        s3_bucket = S3LoggingBucket()
        guid = str(uuid.uuid4().hex)
        path = "%s/%s" % (self.options.log_path, 
                          test.test.id())
        uploaded_files = []
        for logfile in os.listdir(path):
            logfile_name = "%s/%s/%s" % (guid, 
                                       test.test.id(), 
                                       logfile.split(path)[-1])
            s3_bucket.upload_file(logfile_name, 
                                  "%s/%s" % (path, logfile))
            uploaded_files.append(logfile_name)
        s3_bucket.save_uploaded_file_names(uploaded_files)
        index_file = s3_bucket.upload_index_file(test.id(), guid)
        print "Log files uploaded: %s" % index_file
        logging.error("Log files uploaded: %s" % index_file)

        #if the database plugin is running, attach a link to the logs index
        #to the database row
        if hasattr(test.test, "testcase_guid"):
            from test_framework.core.testcase_manager \
                import TestcaseDataPayload, TestcaseManager
            self.testcase_manager = TestcaseManager(self.options.database_env)
            data_payload = TestcaseDataPayload()
            data_payload.guid = test.test.testcase_guid
            data_payload.logURL = index_file
            self.testcase_manager.update_testcase_log_url(data_payload)