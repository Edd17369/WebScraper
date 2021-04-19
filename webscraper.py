from selenium import webdriver
import pyinputplus as pyinp
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv


csv_path = 'C:/Users/faust/OneDrive/Escritorio/jobs.csv'
url_login = 'https://www.linkedin.com/login' 
gecko_path = r'C:/geckodriver/geckodriver.exe' 

class Linkedin():
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options, executable_path=gecko_path)
        self.driver.get(url_login)
        time.sleep(1)
        self.might_jobs = []
        self.login() 
        self.targets = [] # Define targets for jobs       

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
        time.sleep(2)
        try:
            error1 = self.driver.find_element_by_id('error-for-username')
            error2 = self.driver.find_element_by_id('error-for-password')
            if error1.is_displayed():
                print('Error for username')
            elif error2.is_displayed():
                print('Error for password')
            self.driver.find_element_by_id('username').clear()
            self.login()
        except:
            print('Loged!') 


    # Add targets
    def add_target(self, arr): # enter a list
        self.targets.extend(arr)
        
    # View targets
    def show_targets(self):
        if self.targets:
            for target in self.targets:
                print(target)
        else:
            print('No targets')
    
    # Delet targets
    def delet_targets(self):
        self.targets = []

    # Check at least the first 100 jobs
    def search(self, position, location, level):
        if not self.targets:
            print('No targets')
        url = 'https://www.linkedin.com/jobs/search/?f_E=%s&keywords=%s&location=%s' %(level, position, location)
        self.driver.get(url)
        time.sleep(3)
        print('Looking for might jobs...')
        jobs = self.driver.find_elements_by_class_name('jobs-search-results__list-item') #('result-card')
        for page in range(1, 3): # Look for the first 50 offers
            jobs = self.driver.find_elements_by_class_name('jobs-search-results__list-item')#('result-card')
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
                except:
                    continue
                # Look if the job fits the targets
                score = 0
                for target in self.targets:
                    if target in description:
                        score += 1
                if score > 0:
                    try:
                        link = topcard.find_element_by_tag_name('a').get_attribute('href')
                        self.might_jobs.append({'TimeStamp':time.ctime(), 'Title':title, 'Location':location, 'Company':company_name, 'Link':link})
                    except:
                        print(title, end=' ')
                        print('Without link')
                        continue
            next_page = self.driver.find_elements_by_class_name('artdeco-pagination__indicator')
            next_page[page].click()
            time.sleep(2)
        self.driver.quit()
        print('Search finished! %s might jobs founded' % (len(self.might_jobs)))

    def save(self):
        if os.path.isfile(csv_path): 
            csvFile = open(csv_path, 'a', newline='')
            csvDictWriter = csv.DictWriter(csvFile, ['TimeStamp', 'Title', 'Location', 'Company', 'Link'])
        else:
            csvFile = open(csv_path, 'w', newline='')
            csvDictWriter = csv.DictWriter(csvFile, ['TimeStamp', 'Title', 'Location', 'Company', 'Link'])
            csvDictWriter.writeheader()
        for row in self.might_jobs:
            csvDictWriter.writerow(row)
        csvFile.close()
        print('Saved %s' %(csv_path))

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
            self.browser.get(self.might_jobs[0]['Link'])
            for i in range(1, min(n, len(self.might_jobs))):
                self.browser.execute_script("window.open('%s');" %(self.might_jobs[i]['Link']))
                #self.browser.switch_to_window(self.browser.window_handles[-1])           
        else:
            print('No jobs to show! Better lucky next time')


