from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from collections import defaultdict
import os

class Scraper:

    def __init__(self):
        # to keep chrome open
        # chrome_options = Options()
        # chrome_options.add_experimental_option("detach", True)
        # self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = webdriver.Chrome()
        self.driver.get("https://recreation.utoronto.ca")
        self.wait = WebDriverWait(self.driver, 8)


    def click(self, element):
        ActionChains(self.driver).move_to_element(element).click(element).perform()
    
    def xpath_click(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    def xpath_wait_visibility(self, xpath):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
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
        court_bookings_url = '/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[16]/a'
        self.xpath_wait_visibility(court_bookings_url)
        self.xpath_click(court_bookings_url)
    

    def get_court_info(self, court_id):
        '''
        court_id = {1, 2, 3}
        '''

        try:
            court_xpath = f'//*[@id="divBookingProducts-large"]/div[{court_id}]/a'
            self.xpath_wait_visibility(court_xpath)
            self.xpath_click(court_xpath)
        except Exception as e:
            print(e)
            return []

        third_day_xpath = '//*[@id="divBookingDateSelector"]/div[2]/div[2]/button[3]'
        self.xpath_wait_visibility(third_day_xpath)
        self.xpath_click(third_day_xpath)


        day = self.get_xpath_value(third_day_xpath+'/span')

        slot_id = 1
        times = [day]
        while True: 
            try:
                xpath = f'//*[@id="divBookingSlots"]/div[2]/div[{slot_id}]/p/strong'
                times.append(self.get_xpath_value(xpath))
                slot_id += 1
            except Exception as e:
                break
        
        self.driver.back()
        return times


    def scrape_courts(self):
        info_dict = defaultdict(list)

        self.accept_cookies()
        self.login(os.environ.get("USERNAME"), os.environ.get("PASSWORD"))
        self.court_bookings_page()
        
        # correct implementation
        court_id = 1
        while True: 
            try:
                court_name = self.get_xpath_value(f'//*[@id="divBookingProducts-large"]/div[{court_id}]/a/div')

                if 'UTM' in court_name:
                    court_id += 1
                else:
                    info_dict[court_name] = self.get_court_info(court_id)
                    court_id += 1

            except Exception as e:
                break
        
        # for testing purposes

        # for i in range(12, 15):
        #     court_name = self.get_xpath_value(f'//*[@id="divBookingProducts-large"]/div[{i}]/a/div')
        #     info_dict[court_name] = self.get_court_info(i)

        return info_dict

if __name__ == "__main__":
    s = Scraper()
    info_dict = s.scrape_courts()
    print(info_dict)
    # s.court_bookings_page()
    # s.scrape_court(1)