import time
from selenium.webdriver.common.by import By
from utils.DateUtils import DUtils
from utils.LoginUtils import Utils

class AssignmentUtils(Utils):
    @classmethod
    def chooseAssignment(cls, assignmentName):
        cls.driver.find_element(By.XPATH, f"//div[@data-activityname='{assignmentName}']/div/div/div").click()    
        return cls.driver.current_url
    @classmethod
    def submitAssignmentFile(cls, assignmentName, inputFilePath):
        current_url = cls.chooseAssignment(assignmentName)
        time.sleep(2)
        submit_buttons = cls.driver.find_elements(By.XPATH, f"//button[@type='submit']")
        if len(submit_buttons) > 1:
            # Remove submission
            submit_buttons[1].click()
            cls.driver.implicitly_wait(2)
            cls.driver.find_elements(By.XPATH, f"//button[@type='submit']")[1].click()
            cls.driver.implicitly_wait(2)
            cls.driver.get(current_url)
            cls.driver.implicitly_wait(2)
        create_button = cls.driver.find_element(By.XPATH, f"//button[@type='submit']")
        create_button.click()
        cls.driver.implicitly_wait(2)
        cls.driver.find_element(By.CLASS_NAME, "filemanager-container").click()
        cls.driver.implicitly_wait(2)
        inputElement = cls.driver.find_element(By.NAME, "repo_upload_file")
        inputElement.clear()
        inputElement.send_keys(inputFilePath)
        cls.driver.implicitly_wait(2)
        cls.driver.find_element(By.CLASS_NAME, "fp-upload-btn").click()
        time.sleep(5)
    
    @classmethod
    def addAssignment(cls, assignmentName, allowDate, dueDate, remindDate):
        cls.driver.find_element(By.ID, "id_name").send_keys(assignmentName)
        time.sleep(2)
        DUtils.chooseDate("id_allowsubmissionsfromdate_", allowDate)
        DUtils.chooseDate("id_duedate_", dueDate)
        DUtils.chooseDate("id_gradingduedate_", remindDate)
        time.sleep(2)
        cls.driver.find_element(By.ID, "id_submitbutton2").click()
        time.sleep(1)

    @classmethod
    def chooseCourse(cls, courseId, editMode=True):
        cls.driver.get(f'{cls.url}/my/courses.php')
        cls.driver.implicitly_wait(3)
        # driver.find_element(
        #     By.XPATH, "//div[@data-course-id='" + str(courseId) + "']/a"
        # ).click()
        cls.driver.find_element(By.XPATH, "//div[@role='listitem']/a").click()
        time.sleep(2)
        if editMode:
            cls.driver.find_element(By.XPATH, "//input[@name='setmode']").click()
            cls.driver.implicitly_wait(2)

    @classmethod
    def chooseSessionInCourse(cls, sessionId):
        time.sleep(2)
        collapssesection = cls.driver.find_element(
            By.CSS_SELECTOR, "a#collapssesection" + str(sessionId)
        )
        if collapssesection.get_attribute("aria-expanded") == False:
            collapssesection.click()
        time.sleep(2)

        # activity_btn = cls.driver.find_element(
        #     By.CSS_SELECTOR,
        #     "div#coursecontentcollapse" + str(sessionId) + " button",
        # )
        # activity_btn.click()
        cls.driver.find_element(By.XPATH, f"//*[@data-action='open-chooser' and @data-sectionid={str(sessionId)}]").click()        
        time.sleep(2)
        cls.driver.find_element(By.XPATH, "//a[@title='Add a new Assignment']").click()
        time.sleep(2)

    @classmethod
    def deleteSessionInCourse(cls, sessionId):
        dropDowns = cls.driver.find_elements(
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

                cls.driver.find_element(
                    By.CSS_SELECTOR,
                    "div.modal-content > div.modal-footer > button:last-child",
                ).click()
                time.sleep(1)
