"""
This class represents a mock webdriver.  This can be used to unit test code
that requires the existance of a webdriver.  Add methods as needed.
"""
class Firefox():

    def __init__(self):
        print "Yay this is a fake firefox."
        self.browser = "firefox"

    def quit(self):
        print "Horray, we quitted"

    def maximize_window(self):
        print "DAYUM, DIS A BIG WINDOW"

class Remote():

    def __init__(self, arg1, arg2):
        print "Yay this is a fake remote."
        self.arg1 = arg1
        self.arg2 = arg2