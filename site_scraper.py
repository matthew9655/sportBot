from collections import defaultdict
import os
from site_factory import SiteFactory


class Scraper(SiteFactory):
    def get_court_info(self, court_id):

        try:
            court_xpath = f'//*[@id="divBookingProducts-large"]/div[{court_id}]/a'
            self.xpath_wait_visibility(court_xpath, caller='court_xpath')
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
                xpath1 = f'//*[@id="divBookingSlots"]/div[2]/div[{slot_id}]/p/strong'
                xpath2 = f'//*[@id="divBookingSlots"]/div/div[{slot_id}]/p/strong'
                time = self.get_xpath_value(xpath1)
                if time == None:
                    time = self.get_xpath_value(xpath2)
                times.append(time)
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
    s = Scraper(mode='test')
    info_dict = s.scrape_courts()
    print(info_dict)
    # s.court_bookings_page()
    # s.scrape_court(1)