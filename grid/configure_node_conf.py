SELENIUM_SERVER_JAR = "selenium-server-standalone-2.15.0.jar"

GRID_HUB_REGISTER = "http://yourhub.com:4444/hub/register"

GRID_RC_REGISTER = "http://yourotherhub.com:8944/hub/register"

BROWSERS = [
	{
		"browserName": "firefox",
		"version": "3.6",
		"platform": "WINDOWS",
		"maxInstances": "5",
		"javascriptEnabled": "True"
	},
	{
		"browserName": "chrome",
		"platform": "WINDOWS",
		"maxInstances": "3",
		"javascriptEnabled": "True"
	},
	{
		"browserName": "internet explorer",
		"version": "8",
		"platform": "WINDOWS",
		"maxInstances": "1",
		"javascriptEnabled": "True"
	}
]