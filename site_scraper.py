from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Scraper:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://recreation.utoronto.ca")
        self.wait = WebDriverWait(self.driver, 8)


    def click(self, element):
        ActionChains(self.driver).move_to_element(element).click(element).perform()
    
    def xpath_click(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    def xpath_wait_visibility(self, xpath):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def accept_cookies(self):
        cookie_xpath = '//*[@id="gdpr-cookie-accept"]'
        self.xpath_click(cookie_xpath)
    
    
    def login(self, username, password):
        login_xpath = '//*[@id="loginLink"]'
        login = self.wait.until(EC.element_to_be_clickable((By.XPATH, login_xpath)))
        self.click(login)
        #wait for modal for open
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modalLogin"]')))

        print("login modal opened")

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
        court_bookings_url = '/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[16]/a'
        self.xpath_wait_visibility(court_bookings_url)
        self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.xpath_click(court_bookings_url)
    

    def get_court_info(self):
        pass


    def scrape_court(self, court_num):
        court1_xpath = "/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div[2]/div[12]/a"
        court1_css_select = "#divBookingProducts-large > div:nth-child(12) > a:nth-child(1)"
        self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        book_court = self.driver.find_element(By.XPATH, court1_xpath)
        self.click(book_court)

    

def scrape():
    driver = webdriver.Firefox()
    driver.get("https://recreation.utoronto.ca")
    court_bookings_url = '/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[16]/a'

    #actions
    
    driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    court_bookings = driver.find_element(By.XPATH, court_bookings_url)
    ActionChains(driver).move_to_element(court_bookings).click(court_bookings).perform()
    
    # # create actions 
    # actions = ActionChains(driver)
    # # actions.move_to_element(court_bookings)
    # actions.click(court_bookings)
    # actions.perform()

    court1 = "/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div[2]/div[12]/a"
    court2 = ""

if __name__ == "__main__":
    s = Scraper()
    s.accept_cookies()
    s.login('choimat4', 'Matthew9655')
    s.court_bookings_page()
    # s.court_bookings_page()
    # s.scrape_court(1)