class Utils:
    driver = None
    url = None
    
    @classmethod
    def setConfig(cls, driver, url):
        cls.driver = driver
        cls.url = url
