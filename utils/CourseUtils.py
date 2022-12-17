from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from utils.DateUtils import DUtils
from utils.Utils import Utils

class CourseUtils(Utils):
    URLCREATECOURSE = "http://localhost/course/edit.php?category=0"
    URLREMOVECOURSE = "http://localhost/course/management.php"
    REMOVECOURSE_ICON_XPATH = (
        "//a[starts-with(@href, 'http://localhost/course/delete.php')]"
    )
    DELETECOURSE_BTN_XPATH = "//form[@method='post']//button[@type='submit']"

    @classmethod
    def createCourse(cls, fName, sName, startDate, endDate, id):
        cls.driver.get(cls.URLCREATECOURSE)
        # Course FullName
        cls.textFieldHandler(fName, "id_fullname")

        # Course ShortName
        cls.textFieldHandler(sName, "id_shortname")

        # Check for StartDate
        DUtils.chooseDate("id_startdate_", startDate)

        # Check for EndDate
        DUtils.chooseDate("id_enddate_", endDate)

        # Check for Course Id
        courseId = cls.driver.find_element(By.ID, "id_idnumber")
        courseId.clear()
        courseId.send_keys(str(id))
        time.sleep(3)

        # Check SaveAndDisplay Btn
        btnSaveAndDisplay = cls.driver.find_element(By.ID, "id_saveanddisplay")
        btnSaveAndDisplay.click()

        try:
            """Failly Add Course"""
            if cls.driver.find_element(By.ID, "id_saveanddisplay").is_displayed():
                return False
        except NoSuchElementException:
            """Successfully Add Course"""
            return True

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
