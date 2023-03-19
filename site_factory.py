from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from collections import defaultdict
import os

class SiteFactory:

    def __init__(self, mode='op'):
        # to keep chrome open

        chrome_options = Options()
        if mode == 'test':
            chrome_options.add_experimental_option("detach", True)
        else:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("window-size=1400,2100")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://recreation.utoronto.ca")
        self.wait = WebDriverWait(self.driver, 8)


    def click(self, element):
        ActionChains(self.driver).move_to_element(element).click(element).perform()
    
    def xpath_click(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    def xpath_wait_visibility(self, xpath, caller=None):
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutError:
            print(f'element is not visible during {caller} call')
    
    def get_xpath_value(self, xpath):
        return self.driver.find_element(By.XPATH, xpath).text

    def accept_cookies(self):
        cookie_xpath = '//*[@id="gdpr-cookie-accept"]'
        self.xpath_click(cookie_xpath)
    
    
    def login(self, username, password):
        login_xpath = '//*[@id="loginLink"]'
        login = self.wait.until(EC.element_to_be_clickable((By.XPATH, login_xpath)))
        self.click(login)
        #wait for modal for open
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modalLogin"]')))

        button_xpath = '/html/body/div[1]/div/div[3]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[6]/div/button'
        self.xpath_click(button_xpath)

        #input username and password

        self.wait.until(EC.visibility_of_element_located((By.ID, 'username')))

        username_button = self.driver.find_element(By.ID, 'username')
        password_button = self.driver.find_element(By.ID, 'password')

        username_button.send_keys(username)
        password_button.send_keys(password)

        uoft_weblogin_button_xpath = '/html/body/div/div/div[1]/div[2]/form/button'
        self.xpath_click(uoft_weblogin_button_xpath)
    

    def court_bookings_page(self):
        court_bookings_url = '//*[@id="mainContent"]/div[2]/div[1]/div[18]/a'
        self.xpath_wait_visibility(court_bookings_url)
        self.xpath_click(court_bookings_url)