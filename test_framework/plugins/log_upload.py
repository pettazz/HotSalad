"""

Log Upload plugin to upload all logs to a custom server or S3 bucket.

"""

import uuid
import logging
import os

from test_framework.fixtures import constants
from nose.plugins import Plugin


class LogUpload(Plugin):
    """
    The plugin for uploading test logs to a server
    """
    name = 'log_upload'

    #Plugin methods
    def configure(self, options, conf):
        """get the options"""
        super(LogUpload, self).configure(options, conf)
        self.options = options

    def afterTest(self, test):
        """after each testcase, upload its logs to the location specified"""
        index_file = None
        if constants.LogUploader.USE_S3:
            from test_framework.core.s3_manager import S3LoggingBucket

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

        if constants.LogUploader.USE_LOCAL:
            import shutil

            # if the db plugin is enabled, we have an execution guid already
            if hasattr(test.test, "execution_guid"):
                guid = test.test.execution_guid
            else:
                guid = str(uuid.uuid4().hex)
            path = "%s/%s" % (self.options.log_path, 
                              test.test.id())
            # only move logs if they actually exist
            log_files = os.listdir(path)
            if log_files:
                dest_path = "%s/%s" % (constants.LogUploader.DESTINATION_PATH, guid)
                if not os.path.exists(dest_path):
                    os.mkdir(dest_path)
                dest_path = "%s/%s/" % (dest_path, test.test.id())

                shutil.copytree(path, dest_path)
        
                log_files.sort()
                index_str = []
                for logfile in log_files:
                    index_str.append('<a href="%s">%s</a>' % (logfile, logfile))
                index = open(dest_path + 'index.html', 'w')
                index.write("<br>".join(index_str))

                file_name = "%s/%s/index.html" % (guid, test.test.id())
                index_file = "%s%s" % (constants.LogUploader.BASE_URL, file_name)
                print "Log files copied: %s" % index_file
                logging.error("Log files copied: %s" % index_file)

        if index_file:
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