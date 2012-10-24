"""
Script to be run on windows ec2 instances to configure and start the node
server, connected to grid server
"""

import requests
import subprocess

import configure_node_conf as conf

def get_public_hostname():
	"""
	Get the publicly accessible hostname for the node, so we don't try 
	to bind to the external IP.
	"""
	req = requests.get("http://169.254.169.254/latest/meta-data/public-hostname")
	if(req.status_code == requests.codes['\o/']):
		return str(req.content)
	else:
		raise Exception('Couldn\'t get the public nodename!')

def get_browser_string(browser_dict):
	"""
	Convert a dict of Capabilities into a string argument for the node jar
	"""
	str_out = ' -browser "'
	for key in browser_dict.keys():
		str_out += '%s=%s,' % (key, browser_dict[key])
	str_out = str_out[:-1] + '"'
	return str_out

def start_node(nodename):
	"""
	Start the java processe for the node with the appropriate configuration
	"""
	#start the WebDriver Node
	command = "java -jar %s -role node -hub %s -host %s -port 5555" % (
									conf.SELENIUM_SERVER_JAR,
									conf.GRID_HUB_REGISTER,
									nodename)
	for browser in conf.BROWSERS:
		command += get_browser_string(browser)

	subprocess.Popen(command)



if __name__ == '__main__':
	start_node(get_public_hostname())