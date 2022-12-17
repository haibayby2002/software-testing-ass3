import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.AssignmentUtils import AssignmentUtils
from utils.CourseUtils import CourseUtils
from utils.LoginUtils import LoginUtils
from utils.Utils import Utils
from utils.DateUtils import Date

url = "http://localhost"
username = "user"
password = "bitnami"

class UploadFileTestCase(unittest.TestCase):
    courseId = 1
    sessionId = 1
    
    
    def setUp(self) -> None:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        Utils.setConfig(self.driver, url)
        LoginUtils.login(username, password)
        
    def tearDown(self) -> None:
        self.driver.implicitly_wait(1)
        self.driver.close()
        
    def test_1(self) -> None:
        """File submitted exceeds 500MB limit"""
        inputFilePath = os.path.join(os.getcwd(), 'testdata/datagrip.tar.gz')
        assignmentName = "Test 1 Assignment"
        courseId = 1
        allowDate = Date("17", "December", "2022", "8", "30")
        dueDate = Date("25", "December", "2022", "8", "30")
        remindDate = Date("26", "December", "2022", "8", "30")
        CourseUtils.createCourse(
            "Course 1",
            "C1",
            Date("15", "December", "2022", "8", "30"),
            Date("28", "December", "2022", "8", "30"),
            courseId,
        )
        AssignmentUtils.chooseCourse(courseId)
        AssignmentUtils.chooseSessionInCourse(self.sessionId)
        AssignmentUtils.addAssignment(
            assignmentName, allowDate, dueDate, remindDate
        )
        AssignmentUtils.chooseCourse(courseId, editMode=False)
        AssignmentUtils.chooseAssignment(assignmentName)
        AssignmentUtils.submitAssignmentFile(assignmentName, inputFilePath)
        text = self.driver.find_element(By.CLASS_NAME, 'moodle-exception-message').text
        self.assertRegex(text, ".*too large.*")
        AssignmentUtils.deleteSessionInCourse(self.sessionId)
        
    def test_2(self):
        """Drag and drop file to submission"""
        file_name = 'normal_file.txt'
        inputFilePath = os.path.join(os.getcwd(), f'testdata/{file_name}')
        assignmentName = "Test 2 Assignment"
        courseId = 1
        allowDate = Date("17", "December", "2022", "8", "30")
        dueDate = Date("25", "December", "2023", "8", "30")
        remindDate = Date("26", "December", "2023", "8", "30")
        AssignmentUtils.chooseCourse(courseId)
        AssignmentUtils.chooseSessionInCourse(self.sessionId)
        AssignmentUtils.addAssignment(
            assignmentName, allowDate, dueDate, remindDate
        )
        AssignmentUtils.chooseCourse(courseId, editMode=False)
        AssignmentUtils.chooseAssignment(assignmentName)
        AssignmentUtils.submitAssignmentFile(assignmentName, inputFilePath)
        self.driver.find_element(By.ID, "id_submitbutton").click()
        result_rows = self.driver.find_elements(By.CLASS_NAME, 'unselectedrow')
        foundResult = False
        for row in result_rows:
            found_file_name = row.find_element(By.CLASS_NAME, 'c8').text.split('\n')[0]
            status = row.find_element(By.CLASS_NAME, 'c4').text
            if file_name == found_file_name:
                foundResult = True
                self.assertRegex(status, "Submitted.*")
        self.assertTrue(foundResult, "The submitted file not found in result table")
        
    def test_3(self):
        """Normal assignment submission"""
        file_name = 'normal_file.txt'
        inputFilePath = os.path.join(os.getcwd(), f'testdata/{file_name}')
        assignmentName = "Test 3 Assignment"
        courseId = 1
        allowDate = Date("17", "December", "2022", "8", "30")
        dueDate = Date("25", "December", "2023", "8", "30")
        remindDate = Date("26", "December", "2023", "8", "30")
        AssignmentUtils.chooseCourse(courseId)
        AssignmentUtils.chooseSessionInCourse(self.sessionId)
        AssignmentUtils.addAssignment(
            assignmentName, allowDate, dueDate, remindDate
        )
        AssignmentUtils.chooseCourse(courseId, editMode=False)
        AssignmentUtils.chooseAssignment(assignmentName)
        AssignmentUtils.submitAssignmentFile(assignmentName, inputFilePath)
        self.driver.find_element(By.ID, "id_submitbutton").click()
        result_rows = self.driver.find_elements(By.CLASS_NAME, 'unselectedrow')
        foundResult = False
        for row in result_rows:
            found_file_name = row.find_element(By.CLASS_NAME, 'c8').text.split('\n')[0]
            status = row.find_element(By.CLASS_NAME, 'c4').text
            if file_name == found_file_name:
                foundResult = True
                self.assertRegex(status, "Submitted.*")
        self.assertTrue(foundResult, "The submitted file not found in result table")
    
    def test_4(self):
        """No file in submission form"""
        assignmentName = "Test 4 Assignment"
        courseId = 1
        allowDate = Date("17", "December", "2022", "8", "30")
        dueDate = Date("25", "December", "2023", "8", "30")
        remindDate = Date("26", "December", "2023", "8", "30")
        AssignmentUtils.chooseCourse(courseId)
        AssignmentUtils.chooseSessionInCourse(self.sessionId)
        AssignmentUtils.addAssignment(
            assignmentName, allowDate, dueDate, remindDate
        )
        AssignmentUtils.chooseCourse(courseId, editMode=False)
        self.driver.implicitly_wait(2)
        current_url = AssignmentUtils.chooseAssignment(assignmentName)
        time.sleep(2)
        submit_buttons = self.driver.find_elements(By.XPATH, f"//button[@type='submit']")
        if len(submit_buttons) > 1:
            # Remove submission
            submit_buttons[1].click()
            self.driver.implicitly_wait(2)
            self.driver.find_elements(By.XPATH, f"//button[@type='submit']")[1].click()
            self.driver.implicitly_wait(2)
            self.driver.get(current_url)
            self.driver.implicitly_wait(2)
        submit_buttons = self.driver.find_elements(By.XPATH, f"//button[@type='submit']")[0].click()
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.ID, "id_submitbutton").click()
        self.driver.implicitly_wait(2)
        alert_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertRegex(alert_message, "Nothing was submitted.*")

if __name__=="__main__":
    unittest.main()