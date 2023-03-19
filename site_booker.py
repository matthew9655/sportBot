from collections import defaultdict
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from site_factory import SiteFactory

class Booker(SiteFactory):

    def __init__(self, mode):
        SiteFactory.__init__(self, mode) 
        self.wait = WebDriverWait(self.driver, 3)
        self.book()
    
    def xpath_wait_visibility(self, xpath):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def select_court(self, court_id):
        court_xpath = f'//*[@id="divBookingProducts-large"]/div[{court_id}]/a'
        self.xpath_wait_visibility(court_xpath)
        self.xpath_click(court_xpath)
    
    def select_time(self, time_id):
        try:
            time_xpath = f'//*[@id="divBookingSlots"]/div[2]/div[{time_id}]/div/button'
            self.xpath_wait_visibility(time_xpath)
            self.xpath_click(time_xpath)
        except:
            print('booking might be unavailable')
            return

    def book(self):
        self.accept_cookies()
        self.login(os.environ.get("USERNAME"), os.environ.get("PASSWORD"))
        self.court_bookings_page()
        self.select_court(6)
        self.select_time(9)


if __name__ == "__main__":
    Booker(mode='test')
