from selenium.webdriver.common.by import By

class LocatorsManager:

    def __init__(self, driver, locators_dict=None):
        self.driver = driver
        self.locators = {}
        if locators_dict is not None:
            self.add_locators(locators_dict)

    def add_locators(self, locators_dict):
        for x in locators_dict:
            self.add_locator(x, locators_dict[x])

    def add_locator(self, name, locator, locator_type=None):
        if name in self.locators.keys():
            raise Exception('There is an existing locator with the name: %s' % name)
        if locator_type is None:
            if isinstance(locator, tuple):
                locator_type = locator[0]
                locator = locator[1]
            else:
                locator_type = 'CSS_SELECTOR'

        if not hasattr(By, locator_type):
            raise Exception('Unrecognized locator type: %s' % locator_type)

        self.locators[name] = {'type': locator_type, 'locator': locator}

    def find_one(self, obj):
        results = self.find(obj)
        return results[0]

    def find(self, obj):
        if type(obj) == str:
            if obj in self.locators.keys():
                return self.driver.find_elements(getattr(By, self.locators[obj]['type']), self.locators[obj]['locator'])
            else:
                return self.find('CSS_SELECTOR', obj)
        else:
            return self.driver.find_elements(getattr(By, obj[0]), obj[1])

    def get_locator(self, name):
        return self.locators[name]['locator']