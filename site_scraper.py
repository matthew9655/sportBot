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

    def accept_cookies(self):
        cookie_xpath = '//*[@id="gdpr-cookie-accept"]'
        cookie = self.driver.find_element(By.XPATH, cookie_xpath)
        self.click(cookie)
    
    def login(self):
        login_xpath = '//*[@id="loginLink"]'
        login = self.wait.until(EC.element_to_be_clickable((By.XPATH, login_xpath)))
        self.click(login)
        #wait for modal for open
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div[5]/div[1]/div/div/div')))

        print("login modal opened")

        # utorid_button_xpath = '/html/body/div[1]/div/div[3]/div[4]/div[1]/div/div/div/div[2]/div[1]/div[6]/div/button'
        # utorid_button= self.wait.until(EC.element_to_be_clickable((By.XPATH, utorid_button_xpath)))
        # self.click(utorid_button)



    def court_bookings_page(self):
        court_bookings_url = '/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[16]/a'
        self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        court_bookings = self.driver.find_element(By.XPATH, court_bookings_url)
        self.click(court_bookings)


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
    s.login()
    # s.court_bookings_page()
    # s.scrape_court(1)