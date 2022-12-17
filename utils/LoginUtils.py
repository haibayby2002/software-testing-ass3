import time
from selenium.webdriver.common.by import By
from utils.Utils import Utils

class LoginUtils(Utils):
    @classmethod
    def login(cls, username, password):
        cls.driver.get(f"{cls.url}/login/index.php")
        cls.driver.find_element(By.ID, "username").clear()
        cls.driver.find_element(By.ID, "password").clear()
        cls.driver.find_element(By.ID, "username").send_keys(username)
        cls.driver.find_element(By.ID, "password").send_keys(password)
        cls.driver.find_element(By.ID, "loginbtn").click()

    @classmethod
    def logout(cls):
        userMenu = cls.driver.find_element(By.ID, "user-menu-toggle")
        if userMenu.is_displayed():
            userMenu.click()
            cls.driver.find_element(
                By.XPATH,
                f"//a[starts-with(@href, '{cls.url}/login/logout.php')]",
            ).click()
            time.sleep(1)
