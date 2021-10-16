from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

@dataclass
class DailyPass(ABC):
    """Abstract class that will contain daily pass information"""
    # Class Attributes
    student_name : str
    school_name  : str
    qr_code      : str = field(init=False, default='')
    _browserObj  : webdriver.firefox.webdriver.WebDriver = field(init=False, repr=False)

    def __post_init__(self):
        self._browserObj = self.create_headless_browser()

    @abstractmethod
    def navigate_to_pass_site():
        pass

    @abstractmethod
    def log_into_pass_site():
        pass
    
    @abstractmethod
    def create_daily_pass():
        pass

    def create_headless_browser(self) -> webdriver.firefox.webdriver.WebDriver:
        """Create a headless firefox broswer session"""
        try:
            ff_opts = webdriver.FirefoxOptions()
            ff_opts.headless = True
            browser = webdriver.Firefox(options=ff_opts)
        except Exception as err:
            print("Unable to initialize headless FireFox session with Selenium.")
            print(err)
        
        return browser

@dataclass
class LausdPass(DailyPass):
    """LAUSD Daily Pass"""
    pass_url    : str = field(init=False, default='https://pap.lausd.net/en-US/SignIn')

    def navigate_to_pass_site(self) -> None:
        """Set browser location to lausd daily pass login site"""

        print(f"\nNavigating to... {self.pass_url}")
        # Navigate to parents login page
        try:
            self._browserObj.get(self.pass_url)
            parent_sign_in = self._browserObj.find_element(By.ID, 'https://idcs-5143070ce03d415eb20fdc5866138826.identity.oraclecloud.com/')
            parent_sign_in.send_keys(Keys.RETURN)

            # Time delay to allow page load
            time.sleep(5)
        except Exception as err:
            print(f"Unable to access {self.pass_url}")
            print(err)


    def log_into_pass_site(self, user:str, password:str) -> webdriver.firefox.webdriver.WebDriver:
        """Login into daily pass site"""

        print(f"Logging into site as {user}")
        # Grab form elements for login
        username_form = self._browserObj.find_element(By.ID, 'idcs-signin-basic-signin-form-username')
        password_form = self._browserObj.find_element(By.ID, 'idcs-signin-basic-signin-form-password|input')
        sign_in_btn   = self._browserObj.find_element(By.ID, 'idcs-signin-basic-signin-form-submit')
        
        # input credential information
        username_form.send_keys(user)
        password_form.send_keys(password)
        sign_in_btn.click()

        # Check if vaccine prompt is shown at login
        try:
            vaccine_prompt = self._browserObj.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/button')
            vaccine_prompt.click()
        except Exception as err:
            print("No vaccine prompt, continuing execution")
            print(err)
        
        print(f"Successfully logged into {self.pass_url} as {user}")

    def create_daily_pass(self) -> None:
        """Create daily pass QR code"""

        print(f"Creating daily pass for... {self.student_name}")
        
        # Select create pass from menu
        create_pass_btn = self._browserObj.find_element(By.ID, 'create_pass')
        create_pass_btn.click()        
        try:
            # select student
            student_btn = self._browserObj.find_element(By.XPATH, '/html/body/div[5]/button[2]')
            student_btn.click()
        except Exception as err:
            print(f"Unable to select select student... {self.student_name}")
            print(err)
        
        # Provide school information
        school_form = self._browserObj.find_element(By.ID, 'facility')
        school_btn  = self._browserObj.find_element(By.XPATH, '/html/body/form/div[5]/button')
        school_form.send_keys(self.school_name)
        school_btn.click()

        try:
            # sympton/contact validation
            symptons_radio_btn = self._browserObj.find_element(By.ID, 'anycovid19symptoms_0')
            contact_radio_btn  = self._browserObj.find_element(By.ID, 'contactwithCOVID19case_0')
            proceed_btn        = self._browserObj.find_element(By.ID, 'btnProceed')
            
            symptons_radio_btn.click()
            contact_radio_btn.click()
            proceed_btn.click()
            time.sleep(3)
        except Exception as err:
            print("Unable to pass sympton/contact checks")
            print(err)
    
    def share_daily_pass(self, phone: str) -> None:
        """Share daily pass to provided phone number"""

        # This is required to select prior to sharing passing as this element obsecures the share btn. 
        rtsModal = self._browserObj.find_element(By.ID, 'rtsModal')
        rtsModal.click()

        # Share pass button
        share_btn = self._browserObj.find_element(By.XPATH, '/html/body/div[4]/div[5]/a[1]')
        share_btn.click()
        time.sleep(3)
        
        # select input form for email/phone
        share_form = self._browserObj.find_element(By.ID, 'msft_recipient')
        submit_btn = self._browserObj.find_element(By.ID, 'InsertButton')

        # This is required to select prior to sharing passing as this element obsecures the share btn. 
        rtsModal = self._browserObj.find_element(By.ID, 'rtsModal')
        rtsModal.click()

        # Input phone and send message
        share_form.send_keys(phone)
        submit_btn.click()
