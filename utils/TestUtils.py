from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.CourseUtils import CourseUtils
from utils.AssignmentUtils import AssignmentUtils
from utils.LoginUtils import LoginUtils
from utils.DateUtils import Date
import time

class TestAddAssignment:
    @staticmethod
    def test(
        username,
        password,
        courseId,
        sessionId,
        assignmentName,
        allowDate,
        dueDate,
        remindDate,
    ):
        submitStatus = None
        LoginUtils.login(username, password)
        CourseUtils.createCourse(
            "Course 1",
            "C1",
            Date("21", "December", "2022", "8", "30"),
            Date("28", "December", "2022", "8", "30"),
            courseId,
        )
        AssignmentUtils.chooseCourse(courseId)
        AssignmentUtils.chooseSessionInCourse(sessionId)
        AssignmentUtils.addAssignment(
            assignmentName, allowDate, dueDate, remindDate
        )
        AssignmentUtils.deleteSessionInCourse(sessionId)

        try:
            """Submit assignment fail"""
            if driver.find_element(By.ID, "id_submitbutton2").is_displayed():
                submitStatus = False
        except NoSuchElementException:
            """Submit assignment successfully"""
            submitStatus = True

        CourseUtils.removeCourse()

        LUtils.logout()
        return submitStatus

    @staticmethod
    def chooseCourse(courseId):
        driver.find_element(By.XPATH, "//li[@data-key='mycourses']/a").click()
        driver.implicitly_wait(2)
        driver.find_element(
            By.XPATH, "//div[@data-course-id='" + str(courseId) + "']/a"
        ).click()
        time.sleep(2)
    
        driver.find_element(By.XPATH, "//input[@name='setmode']").click()
        driver.implicitly_wait(2)
    
    @staticmethod
    def chooseSessionInCourse(sessionId):
        collapssesection = driver.find_element(
            By.CSS_SELECTOR, "a#collapssesection" + str(sessionId)
        )
        if collapssesection.get_attribute("aria-expanded") == False:
            collapssesection.click()
        time.sleep(2)
    
        activity_btn = driver.find_element(
            By.CSS_SELECTOR,
            "div#coursecontentcollapse" + str(sessionId) + " button",
        )
        activity_btn.click()
        time.sleep(2)
    
        driver.find_element(By.XPATH, "//a[@title='Add a new Assignment']").click()
    time.sleep(2)

    @staticmethod
    def deleteSessionInCourse(sessionId):
        dropDowns = driver.find_elements(
            By.CSS_SELECTOR,
            "div#coursecontentcollapse" + str(sessionId) + " div.dropdown",
        )
        for drop in dropDowns:
            if drop.is_displayed():
                drop.find_element(By.CSS_SELECTOR, "a").click()
                time.sleep(1)
    
                drop.find_element(
                    By.CSS_SELECTOR,
                    "div.dropdown-menu > a.editing_delete",
                ).click()
                time.sleep(1)
    
                driver.find_element(
                    By.CSS_SELECTOR,
                    "div.modal-content > div.modal-footer > button:last-child",
                ).click()
    
                time.sleep(1)

    @staticmethod
    def chooseDate(selectElId, date):
        for value in ["day", "month", "year", "hour", "minute"]:
            selectOptionsHandler(
                driver.find_element(By.ID, selectElId + value),
                date[value],
            )

    @staticmethod
    def addAssignment(assignmentName, allowDate, dueDate, remindDate):
        driver.find_element(By.ID, "id_name").send_keys(assignmentName)
        time.sleep(2)
    
        TestAddAssignment.chooseDate("id_allowsubmissionsfromdate_", allowDate)
        TestAddAssignment.chooseDate("id_duedate_", dueDate)
        TestAddAssignment.chooseDate("id_gradingduedate_", remindDate)
        time.sleep(2)
    
        driver.find_element(By.ID, "id_submitbutton2").click()
        time.sleep(2)


class Date:
    def __init__(self, day, month, year, hour, minute):
        self.day = day
        self.month = month
        self.year = year
        self.hour = hour
        self.minute = minute

    def __getitem__(self, item):
        return getattr(self, item)
