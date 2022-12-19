from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
# from utils.DateUtils import DUtils
from utils.Utils import Utils
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

# CSS Selector: #yui_3_17_2_1_1671370578806_243 > div.d-md-inline-block.mr-md-2.position-relative > input

class EnrollCourseUtils(Utils):
    # URLCREATECOURSE = "http://localhost/course/edit.php?category=0"
    # URLREMOVECOURSE = "http://localhost/course/management.php"
    # REMOVECOURSE_ICON_XPATH = (
    #     "//a[starts-with(@href, 'http://localhost/course/delete.php')]"
    # )
    # DELETECOURSE_BTN_XPATH = "//form[@method='post']//button[@type='submit']"



    URL_ENROLL_COURSE = "http://localhost/user/index.php?"
    # f'Hello, {name}!'
    @classmethod
    def enrollCourse(cls, list_mail, course_id):
        cls.driver.get(f'{cls.URL_ENROLL_COURSE}id={str(course_id)}')

        cls.driver.find_element(By.ID, "enrolusersbutton-1").click()   #Button


        # cls.driver.find_element(By.XPATH, '''//input[@type='text']''')
        cls.driver.implicitly_wait(5)

        search = cls.driver.find_element(By.XPATH, '//div[@class="d-md-inline-block mr-md-2 position-relative"]/input')

        # Toi day ok

        # //div[@class="d-md-inline-block mr-md-2 position-relative"]/input

        # el = driver.findElement(By.xpath("//div[@id = 'colLeft_OrderGroups']/descendant::li[text() = '" + text + "']"))
        print(search)
        for mail in list_mail:
            search.clear()
            search.send_keys(mail)
            first_result = cls.driver.find_element(By.XPATH,
                "//ul[@class='form-autocomplete-suggestions']/li[1]"
            )
            first_result.click()
            time.sleep(5)
        # Enter
        btnSubmit = cls.driver.find_element(By.XPATH, "//button[text()='Enrol users']")
        btnSubmit.click()
        
        time.sleep(5)

        enrolls_mails = cls.driver.find_elements(By.XPATH, "//td[@class='cell c2']")
        count = len(list_mail)
        for i in enrolls_mails:
            email = i.text
            print(email)
            if email in list_mail:
                count=count-1
        return count==0

        # //div[@class=toast-wrapper
       
        

        return True

    @classmethod
    def textFieldHandler(cls, value, fieldId):
        textEl = cls.driver.find_element(By.ID, fieldId)
        textEl.clear()
        textEl.send_keys(str(value))

    @classmethod
    def UnEnrollCOurse(cls):
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
