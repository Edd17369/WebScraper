from selenium import webdriver
import pyinputplus as pyinp
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv

# Experience with multiple testing methods such as: smoke tests, black-box, white-box, gray-box, boundary testing.
url = 'https://www.linkedin.com/jobs/search/?f_E=2&f_WRA=true&geoId=92000000&keywords=software%20engineer&location=Worldwide&sortBy=DD&position=1&pageNum=0'
url_login = 'https://www.linkedin.com/login' 
csv_path = 'C:/Users/faust/OneDrive/Escritorio/jobs.csv'
gecko_path = r'C:/geckodriver/geckodriver.exe'

class Linkedin():
    def __init__(self):
        options = Options()
        options.headless = True
        #self.driver = webdriver.Firefox(options=options, executable_path=r'C:/geckodriver/geckodriver.exe')
        self.driver = webdriver.Firefox(executable_path=gecko_path)
        self.driver.get(url_login)
        self.might_jobs = []
        self.login()        
        self.targets = ['python', 'django'] # Define targets for jobs
        if os.path.isfile(csv_path): 
            self.csvFile = open(csv_path, 'a')
            self.csvDictWriter = csv.DictWriter(self.csvFile, ['TimeStamp', 'Title', 'Location', 'Company'])
        else:
            self.csvFile = open(csv_path, 'w', newline='')
            self.csvDictWriter = csv.DictWriter(self.csvFile, ['TimeStamp', 'Title', 'Location', 'Company'])
            self.csvDictWriter.writeheader()

    def login(self):
        try:
            username_input = self.driver.find_element_by_id('username')
            password_input = self.driver.find_element_by_id('password')
            login_input = self.driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[3]/button')
        except Exception as exc:
            print('%s' % (exc))
        username = pyinp.inputStr(prompt='Username: ')
        password = pyinp.inputPassword(prompt='Password: ')
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_input.click()
        

    # View targets
    # Edit new targets

    # Check at least the first 100 jobs
    def search(self):
        self.driver.get(url)
        time.sleep(3)
        print('Looking for might jobs...')
        html = self.driver.find_element_by_tag_name('html')
        jobs = self.driver.find_elements_by_class_name('jobs-search-results__list-item') #('result-card')
        while len(jobs) < 10:
            html.send_keys(Keys.END)
            time.sleep(1)#self.driver.implicitly_wait(1)
            jobs = self.driver.find_elements_by_class_name('jobs-search-results__list-item')#('result-card')
            
        # Look jobs that fit the targets
        for job in jobs:
            job.click()
            time.sleep(1)
            try:
                detail = self.driver.find_element_by_class_name('jobs-search__job-details--container')#('results__detail-view')
                description = detail.find_element_by_class_name('jobs-description__content').text.lower()#('description').text.lower()
                topcard = detail.find_element_by_class_name('jobs-details-top-card__content-container')#('topcard__content-left')
                title = topcard.find_element_by_class_name('jobs-details-top-card__job-title').text#('topcard__title').text
                company = topcard.find_element_by_class_name('jobs-details-top-card__company-info')#('topcard__flavor')[0].text 
                try:
                    company_name = company.find_element_by_tag_name('a').text
                except:
                    company_name = company.text
                location = topcard.find_element_by_class_name('jobs-details-top-card__bullet').text#('topcard__flavor')[1].text
                self.csvDictWriter.writerow({'TimetStamp':time.ctime(), 'Title':title, 'Location':location, 'Company':company} )       
            except:
                continue
            score = 0
            for target in self.targets:
                if target in description:
                    score += 1
            if score > 0:
                try:
                    link = topcard.find_element_by_tag_name('a').get_attribute('href')
                    self.might_jobs.append(link)
                    #self.might_jobs.append({'TimetStamp':time.ctime(), 'Title':title, 'Location':location, 'Company':company, 'Link':link})
                except:
                    print(title, end=' ')
                    print('Without link')
                    continue
        self.csvFile.close()
        self.driver.quit()
        print('Search finished! %s might jobs founded' % (len(self.might_jobs)))

    # Open driver with at most n first jobs
    def show(self, n):
        if self.might_jobs:
            self.browser = webdriver.Firefox(executable_path=gecko_path)
            #self.browser.get(url_login)
            #time.sleep(1)
            #self.login()
            #try:
            #    wait = WebDriverWait(self.browser, 20).until(EC.title_contains('Feed'))
            #except:
            #    print("You aren't loged")
            self.browser.get(self.might_jobs[0])
            for i in range(1, min(n, len(self.might_jobs))):
                self.browser.execute_script("window.open('%s');" %(self.might_jobs[i]))
                #self.browser.switch_to_window(self.browser.window_handles[-1])           
        else:
            print('No jobs to show! Better lucky next time')


