# table delayedTestData
# -----------------------------------
CREATE TABLE `delayedTestData` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `testcaseAddress` varchar(1024) NOT NULL DEFAULT '',
  `insertedAt` bigint(20) NOT NULL,
  `expectedResult` text,
  `done` tinyint(1) DEFAULT '0',
  `expiresAt` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`guid`),
  UNIQUE KEY `uuid` (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# table exception
# -----------------------------------
CREATE TABLE `exception` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `hash` varchar(64) NOT NULL DEFAULT '',
  `text` text,
  `jiraIssue` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

# table execution
# -----------------------------------
CREATE TABLE `execution` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `totalExecutionTime` int(11) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `executionStart` bigint(20) DEFAULT '0',
  PRIMARY KEY (`guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

# table testcaseRunData
# -----------------------------------
CREATE TABLE `testcaseRunData` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `testcaseAddress` varchar(1024) DEFAULT NULL,
  `application` varchar(1024) DEFAULT NULL,
  `execution_guid` varchar(64) DEFAULT NULL,
  `runtime` int(11) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `browser` varchar(255) DEFAULT NULL,
  `retryCount` int(11) DEFAULT '0',
  `exception_guid` varchar(64) DEFAULT NULL,
  `environment` varchar(32) DEFAULT '',
  `logURL` text,
  `sauceJobID` varchar(64) DEFAULT NULL,
  `message` text,
  `startTime` bigint(15) DEFAULT '0',
  PRIMARY KEY (`guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;