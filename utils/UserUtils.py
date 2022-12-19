# http://localhost/user/editadvanced.php?id=-1
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from utils.DateUtils import DUtils
from utils.Utils import Utils
from utils.LoginUtils import LoginUtils

class UserUtils(Utils):
    URLCREATEUSER = "http://localhost/user/editadvanced.php?id=-1"
    URLREMOVEUSER = "http://localhost/course/management.php"
    REMOVECOURSE_ICON_XPATH = (
        "//a[starts-with(@href, 'http://localhost/course/delete.php')]"
    )
    DELETEUSER_BTN_XPATH = "//form[@method='post']//button[@type='submit']"

    @classmethod
    def createUser(cls, username, password, fname, sname, email):
        try:
            cls.driver.find_element(By.ID, 'loginbtn')
            cls.driver.find_element(By.ID, "username").clear()
            cls.driver.find_element(By.ID, "password").clear()
            cls.driver.find_element(By.ID, "username").send_keys(username)
            cls.driver.find_element(By.ID, "password").send_keys(password)
            cls.driver.find_element(By.ID, "loginbtn").click()
        except NoSuchElementException:
            pass 
    
        cls.driver.get(cls.URLCREATEUSER)
        # User name
        cls.textFieldHandler(username, "id_username")

        # Password
        hidden = cls.driver.find_element(By.XPATH, '''//a[@data-passwordunmask='edit']''')
        hidden.click()
        
        cls.driver.implicitly_wait(5)
        cls.driver.find_element(By.ID, "id_newpassword").send_keys(password)      #Check this out --------------------------------------------------

        # First name
        cls.textFieldHandler(fname, "id_firstname")

        # Sur name
        cls.textFieldHandler(sname, "id_lastname")

        # Email
        cls.textFieldHandler(email, "id_email")

    

        # Check SaveAndDisplay Btn
        btnSaveAndDisplay = cls.driver.find_element(By.ID, "id_submitbutton")
        btnSaveAndDisplay.click()

        try:
            """Failly Add Course"""
            if cls.driver.find_element(By.CSS_SELECTOR, "#user-notifications > div").is_displayed():
                return True
        except NoSuchElementException:
            """Successfully Add Course"""
            return False

    @classmethod
    def textFieldHandler(cls, value, fieldId):
        textEl = cls.driver.find_element(By.ID, fieldId)
        textEl.clear()
        textEl.send_keys(str(value))

    @classmethod
    def removeCourse(cls):
        cls.driver.get(cls.URLREMOVECOURSE)

        try:
            icon = cls.driver.find_element(
                By.XPATH, cls.REMOVECOURSE_ICON_XPATH
            )
            if icon.is_displayed():
                time.sleep(0.5)
                icon.click()
                time.sleep(0.5)
                cls.driver.find_element(
                    By.XPATH, cls.DELETECOURSE_BTN_XPATH
                ).click()
                cls.driver.get(cls.URLREMOVECOURSE)
                return True
        except NoSuchElementException:
            return False