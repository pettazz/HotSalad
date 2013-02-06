from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Locator:
    """
    Represents an instance of a Locator for some webelement
    """
    def __init__(self, webdriver, key_name, locator, by=By.CSS_SELECTOR):
        self.driver = webdriver
        self.key_name = key_name
        self.locator = locator
        self.by = by

    def __str__(self):
        return "%s (%s)" % (self.key_name, self.locator)

    def find(self):
        """
        Find all instances that are identified by this locator
        @returns
        webelement or list of webelements
        """
        return self.driver.find_elements(getattr(By, self.by), self.locator)
    
    def find_one(self):
        """
        Find exactly one instance identified by this locator. If multiple elements are found, returns the
        first in the list.
        @returns
        webelement identified by this locator.
        """
        results = self.driver.find_elements(getattr(By, self.by), self.locator)
        if len(results) == 0:
            raise NoSuchElementException('Locator `%s` (%s) not found.' % (self.key_name, self.locator))
        return results[0]


class LocatorsManager:
    """
    Helper class for creating and working with Locator instances
    """
    def __init__(self, driver, locators_dict=None):
        self.driver = driver
        self.locators = {}
        if locators_dict is not None:
            self.add_locators(locators_dict)

    def __getattr__(self, name):
        """
        Allows us to access Locator instances stored within the helper directly as attributes
        """
        if name in self.locators.keys():
            return self.locators[name]
        else:
            raise Exception('Locator `%s` not found' % name)

    def add_locators(self, locators_dict):
        """
        Add the given locators to the list of instances.
        @params
        locators_dict - Dictionary of Locators to be added where each key is the Locator name
                        and each value is the corresponding Locator instance
        """
        for x in locators_dict:
            self.add_locator(x, locators_dict[x])

    def add_locator(self, name, locator, locator_type=None):
        """
        Add a single Locator to the list of instances. If not already a Locator instance, 
        it will be instantiated as one.
        @params
        name - name of the Locator
        locator - one of: Locator instance to be added,
                          tuple containing (value, locator type)
                          String locator value
        locator_type - String type of locator that is being added, as enumerated 
                       in selenium.webdriver.common.by:By. one of:
                            CSS_SELECTOR  (default)
                            CLASS_NAME
                            ID
                            NAME
                            LINK_TEXT
                            XPATH
                            TAG_NAME
                            PARTIAL_LINK_TEXT
        """
        if name in self.locators.keys():
            raise Exception('There is an existing locator with the name: %s' % name)
        if isinstance(locator, Locator):
            self.locators[name] = locator
        else:
            if locator_type is None:
                if isinstance(locator, tuple):
                    locator_type = locator[0]
                    locator = locator[1]
                else:
                    locator_type = 'CSS_SELECTOR'

            if not hasattr(By, locator_type):
                raise Exception('Unrecognized locator type: %s' % locator_type)

            self.locators[name] = Locator(self.driver, name, locator, locator_type)

    def find_one(self, locator):
        """
        Find exactly one instance identified by this locator. If multiple elements are found, returns the
        first in the list.
        @params
        locator - one of: String Locator instance name
                          String locator definition (using By.CSS_SELECTOR)
                          tuple locator containing (value, locator type)
        @returns
        webelement identified by this locator.
        """
        results = self.find(locator)
        if len(results) == 0:
            raise Exception('Locator `%s` not found' % locator)
        return results[0]

    def find(self, locator):
        """
        Find all instances that are identified by this locator
        @params 
        locator - one of: String Locator instance name
                          String locator definition (using By.CSS_SELECTOR)
                          tuple locator containing (value, locator type)
        @returns
        webelement or list of webelements
        """
        if type(locator) == str:
            # a string definition key was passed in
            if locator in self.locators.keys():
                # we have a definition for this locator key
                #return self.driver.find_elements(getattr(By, self.locators[locator].by), self.locators[locator].locator)
                return self.locators[locator].find()
            else:
                # default to By.CSS_SELECTOR if we don't recognize it
                return self.find(('CSS_SELECTOR', locator))
        else:
            # a tuple definition was passed in
            return self.driver.find_elements(getattr(By, obj[0]), obj[1])

    def find_child(self, webelement, locator):
        """
        Find exactly one instance that is a child of the given webelement, identified by this locator. 
        If multiple elements are found, returns the first in the list.
        @params
        locator - one of: String Locator instance name
                          String locator definition (using By.CSS_SELECTOR)
                          tuple locator containing (value, locator type)
        @returns
        webelement identified by this locator.
        """
        results = self.find_children(webelement, locator)
        if len(results) == 0:
            raise Exception('Locator `%s` not found' % locator)
        return results[0]

    def find_children(self, webelement, locator):
        """
        Find all instances that are children of a given webelement, identified by this locator.
        @params 
        locator - one of: String Locator instance name
                          String locator definition (using By.CSS_SELECTOR)
                          tuple locator containing (value, locator type)
        @returns
        webelement or list of webelements
        """
        if type(locator) == str:
            # a string definition key was passed in
            if locator in self.locators.keys():
                # we have a definition for this locator key
                return webelement.find_elements(getattr(By, self.locators[locator].by), self.locators[locator].locator)
            else:
                # default to By.CSS_SELECTOR if we don't recognize it
                return self.find_children(webelement, ('CSS_SELECTOR', locator))
        else:
            # a tuple definition was passed in
            return webelement.find_elements(getattr(By, obj[0]), obj[1])

    def get_locator(self, name):
        """
        Return the raw locator value of a given Locator name
        @params
        name - name of the Locator instance
        @returns
        String value of the locator, regardless of locator type.
        """
        return self.locators[name].locator